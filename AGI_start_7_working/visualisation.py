import json
from html import escape
import colorsys

def generate_color_scheme(num_colors):
    return [colorsys.hsv_to_rgb(i / num_colors, 0.8, 0.8) for i in range(num_colors)]

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(int(x * 255) for x in rgb)

def create_modelium_vis_js(modelium_configs):
    nodes = []
    edges = []
    groups = set()
    chains = set()

    for config_index, modelium_config in enumerate(modelium_configs):
        # Access the 'model_config' list directly
        model_configs = modelium_config['model_config']
        loop_level = 0  # Initialize loop level for each chain config

        for chain_index, config in enumerate(model_configs):
            chains.add(chain_index)
            groups.add(config['model_type'])

            node_id = f"{chain_index}_{config['model_name']}_{loop_level}"  # Include loop level
            node = {
                "id": node_id,
                "label": config["model_name"],
                "group": config["model_type"],
                "title": f"<strong>{config['model_name']}</strong><br>"
                         f"<b>Type:</b> {config['model_type']}<br>"
                         f"<b>Access:</b> {config['model_access']}<br>"
                         f"<b>Tool:</b> {config['tool_access']}<br>"
                         f"<b>Check Flags:</b> {config['check_flags']}<br>"
                         f"<b>System Instruction:</b> {escape(config['system_instruction'])}<br>"
                         f"<b>Prompt:</b> {escape(config['prompt'])}",
                "x": chain_index * 300,  # Separate chains horizontally
                "y": (len(model_configs) * loop_level + config.get('level', 0)) * 200,  # Vertical positioning with loop level
                "level": config.get('level', 0),
                "chainIndex": chain_index,
                "modelType": config['model_type'],
                "toolAccess": config['tool_access'],
                "checkFlags": config['check_flags'],
                "chain": chain_index
            }

            if config["tool_access"] != "none":
                node["shape"] = "diamond"
            if config["check_flags"]:
                node["borderWidth"] = 3
                node["borderWidthSelected"] = 5

            nodes.append(node)

            if config["model_access"] != "none":
                parent_id = f"{chain_index}_{config['model_access']}_{loop_level}"  # Include loop level
                edges.append({
                    "from": parent_id,
                    "to": node_id,
                    "arrows": "to"
                })

            # Add loop edge connecting to the next loop level
            if config.get("loop_to_start", False) and loop_level < int(modelium_config['max_number_of_loops_in_run']):
                first_node_id = f"{chain_index}_{model_configs[0]['model_name']}_{loop_level + 1}"  # Next loop level
                edges.append({
                    "from": node_id,  # From the last node of the current level
                    "to": first_node_id,
                    "arrows": "to",
                    "dashes": True,
                    "label": "Loop"
                })
                loop_level += 1  # Increment loop level for the next iteration

            # Add return node for the last node in the chain
            if chain_index == len(model_configs) - 1:
                return_node_id = f"return_{chain_index}_{loop_level}"
                nodes.append({
                    "id": return_node_id,
                    "label": "Return",
                    "x": chain_index * 300,
                    "y": (len(model_configs) * (loop_level + 1)) * 200,  # Position below the last loop iteration
                    "shape": "ellipse",  # You can customize the shape
                    "color": "lightgreen" # You can customize the color
                })
                edges.append({
                    "from": node_id,
                    "to": return_node_id,
                    "arrows": "to"
                })
    vis_data = {
        "nodes": nodes,
        "edges": edges
    }

    color_palette = generate_color_scheme(len(groups))
    group_colors = {group: rgb_to_hex(color) for group, color in zip(groups, color_palette)}

    chain_color_palette = generate_color_scheme(len(chains))
    chain_colors = {chain: rgb_to_hex(color) for chain, color in zip(chains, chain_color_palette)}

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dynamic Modelium Visualization</title>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style type="text/css">
            body, html {{
                height: 100%;
                margin: 0;
                padding: 0;
                overflow: hidden;
                font-family: Arial, sans-serif;
            }}
            #mynetwork {{
                width: 80%;
                height: 100%;
                float: left;
            }}
            #sidebar {{
                width: 20%;
                height: 100%;
                float: right;
                padding: 10px;
                box-sizing: border-box;
                overflow-y: auto;
                background-color: #f0f0f0;
            }}
            #controls, #configInput {{
                margin-bottom: 20px;
            }}
            #legend {{
                margin-bottom: 20px;
            }}
            .legend-item {{
                margin-bottom: 5px;
            }}
            #nodeInfo {{
                margin-top: 20px;
            }}
            #statsChart {{
                margin-top: 20px;
            }}
            textarea {{
                width: 100%;
                height: 200px;
            }}
        </style>
    </head>
    <body>
    <div id="mynetwork"></div>
    <div id="sidebar">
        <div id="configInput">
            <h3>New Configuration</h3>
            <textarea id="newConfig" placeholder="Paste your new modelium_config here"></textarea>
            <button onclick="updateVisualization()">Update Visualization</button>
        </div>
        <div id="controls">
            <h3>Display Options</h3>
            <label><input type="checkbox" id="showModelType" checked> Show Model Type</label><br>
            <label><input type="checkbox" id="showToolAccess"> Show Tool Access</label><br>
            <label><input type="checkbox" id="showCheckFlags"> Show Check Flags</label><br>
            <label>
                Layout:
                <select id="layoutSelect">
                    <option value="hierarchical">Hierarchical</option>
                    <option value="standard">Standard</option>
                </select>
            </label><br>
            <label>
                Color Scheme:
                <select id="colorSchemeSelect">
                    <option value="modelType">By Model Type</option>
                    <option value="chain">By Chain</option>
                </select>
            </label><br>
            <label><input type="checkbox" id="preventOverlap"> Prevent Overlap</label>
        </div>
        <div id="legend">
            <h3>Legend</h3>
            <div class="legend-item">🔹 Standard Model</div>
            <div class="legend-item">🔶 Model with Tool Access</div>
            <div class="legend-item">🔷 Model with Check Flags</div>
            <div class="legend-item">➡️ Model Access Flow</div>
            <div class="legend-item">➿ Looping Chain</div>
        </div>
        <div id="nodeInfo">
            <h3>Selected Node Info</h3>
            <p>Click on a node to see details</p>
        </div>
        <div id="statsChart">
            <canvas id="myChart"></canvas>
        </div>
    </div>
    <script type="text/javascript">
        var container = document.getElementById('mynetwork');
        var data = {json.dumps(vis_data)};
        var groupColors = {json.dumps(group_colors)};
        var chainColors = {json.dumps(chain_colors)};

        var options = {{
            layout: {{
                hierarchical: {{
                    enabled: true,
                    direction: 'UD',
                    sortMethod: 'directed',
                    levelSeparation: 150
                }}
            }},
            physics: {{
                enabled: false
            }},
            nodes: {{
                shape: 'box',
                margin: 10,
                widthConstraint: {{
                    minimum: 120,
                    maximum: 250
                }},
                font: {{
                    size: 16
                }}
            }},
            edges: {{
                smooth: {{
                    type: 'cubicBezier',
                    forceDirection: 'vertical',
                    roundness: 0.4
                }}
            }},
            groups: groupColors,
            interaction: {{
                hover: true,
                zoomView: true,
                dragView: true
            }}
        }};

        var network = new vis.Network(container, data, options);

        function updateNodeLabels() {{
            var showModelType = document.getElementById('showModelType').checked;
            var showToolAccess = document.getElementById('showToolAccess').checked;
            var showCheckFlags = document.getElementById('showCheckFlags').checked;

            data.nodes.forEach(function(node) {{
                var label = node.label;
                if (showModelType) label += '\\n' + node.modelType;
                if (showToolAccess) label += '\\n' + (node.toolAccess !== 'none' ? '🔧' : '');
                if (showCheckFlags) label += '\\n' + (node.checkFlags ? '✅' : '');
                node.label = label.trim();
            }});

            network.setData({{nodes: data.nodes, edges: data.edges}});
        }}

        function updateColorScheme() {{
            var colorScheme = document.getElementById('colorSchemeSelect').value;
            var colors = colorScheme === 'modelType' ? groupColors : chainColors;
            var colorKey = colorScheme === 'modelType' ? 'group' : 'chain';

            data.nodes.forEach(function(node) {{
                node.color = colors[node[colorKey]];
            }});

            network.setData({{nodes: data.nodes, edges: data.edges}});
        }}

        function toggleOverlapPrevention() {{
            var preventOverlap = document.getElementById('preventOverlap').checked;
            network.setOptions({{
                physics: {{
                    enabled: preventOverlap,
                    repulsion: {{
                        nodeDistance: 150
                    }}
                }}
            }});
        }}

        document.getElementById('showModelType').addEventListener('change', updateNodeLabels);
        document.getElementById('showToolAccess').addEventListener('change', updateNodeLabels);
        document.getElementById('showCheckFlags').addEventListener('change', updateNodeLabels);
        document.getElementById('colorSchemeSelect').addEventListener('change', updateColorScheme);
        document.getElementById('preventOverlap').addEventListener('change', toggleOverlapPrevention);

        document.getElementById('layoutSelect').addEventListener('change', function(event) {{
            var layout = event.target.value;
            if (layout === 'hierarchical') {{
                network.setOptions({{ layout: {{ hierarchical: {{ enabled: true }} }} }});
            }} else {{
                network.setOptions({{ layout: {{ hierarchical: {{ enabled: false }} }} }});
            }}
        }});

        network.on("selectNode", function(params) {{
            var nodeId = params.nodes[0];
            var node = network.body.data.nodes.get(nodeId);
            document.getElementById('nodeInfo').innerHTML = '<h3>' + node.label + '</h3>' + node.title;
            updateChart(node);
        }});

        function updateChart(node) {{
            var ctx = document.getElementById('myChart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['Chain Index', 'Level'],
                    datasets: [{{
                        label: 'Node Position',
                        data: [node.chainIndex, node.level],
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.6)',
                            'rgba(153, 102, 255, 0.6)'
                        ]
                    }}]
                }},
                options: {{
                    scales: {{
                        y: {{
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
        }}

        network.on("afterDrawing", function (ctx) {{
            network.fit({{
                animation: {{
                    duration: 1000,
                    easingFunction: 'easeOutQuint'
                }}
            }});
        }});

        network.on("doubleClick", function(params) {{
            if (params.nodes.length > 0) {{
                network.focus(params.nodes[0], {{
                    scale: 1.5,
                    animation: {{
                        duration: 1000,
                        easingFunction: 'easeOutQuint'
                    }}
                }});
            }}
        }});

        function updateVisualization() {{
            var newConfigText = document.getElementById('newConfig').value;
            try {{
                var newConfig = JSON.parse(newConfigText);
                // Here you would process the new config and update the visualization
                // For demonstration, we'll just log it to the console
                console.log("New configuration received:", newConfig);
                alert("New configuration received. Check the console for details.");
                // In a real implementation, you would update the 'data' variable and redraw the network
            }} catch (error) {{
                alert("Error parsing JSON: " + error.message);
            }}
        }}
    </script>
    </body>
    </html>
    """
    with open("dynamic_modelium_visualization.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Dynamic Modelium visualization saved to dynamic_modelium_visualization.html")
    return html