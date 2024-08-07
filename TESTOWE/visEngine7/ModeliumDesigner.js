'use strict';

// 1. Data Structures and Initialization

let nodes = new vis.DataSet([]);
let edges = new vis.DataSet([]);
let network = null;
let lastNodeId = 0;

// 2. Presets and Data

const promptsData = [
    {
        "id": "prompt_root",
        "text": "Prompts",
        "children": [
            {
                "id": "sys_general_1",
                "text": "General System Prompt 1",
                "content": "You are a helpful and harmless AI assistant."
            },
            {
                "id": "prompt_i_1",
                "text": "Image Generation Prompt 1",
                "content": "Generate an image of a [subject] in the style of [artist]."
            }
        ]
    }
];

const presets = {
    models: [
        {
            id: 'gpt-3.5-turbo',
            name: 'GPT-3.5 Turbo',
            type: 'Generative Language Model',
            icon: '🤖',
            nickName: "GPT-3.5 Turbo",
            prompts: ['sys_general_1'],
            system_instructions: "You are a helpful assistant.",
            tools: "none",
            modelType: "Generative Language Model"
        },
        {
            id: 'dalle-2',
            name: 'DALL-E 2',
            type: 'Image Generation Model',
            icon: '🎨',
            nickName: "DALL-E 2",
            prompts: ['prompt_i_1'],
            system_instructions: "Generate an image based on the given prompt.",
            tools: "none",
            modelType: "Image Generation Model"
        }
    ],
    modeliums: [
        {
            name: 'Simple Chain',
            chainLength: 3,
            loopCount: 0,
            parallelCount: 1,
            modeliumType: 'standard',
            structureDescription: "",
            nestedModeliums: []
        },
        {
            name: 'Chain with Loop',
            chainLength: 2,
            loopCount: 3,
            parallelCount: 1,
            modeliumType: 'chainLoop',
            structureDescription: "",
            nestedModeliums: []
        }
    ]
};

const modelTypes = [
    "Text",
    "Image",
    "Audio",
    "Video",
    "Text to Audio",
    "Image Generation",
    // Add more as needed
];

// 3. Network Initialization

function initNetwork() {
    const container = document.getElementById('modelium-container');
    const data = { nodes: nodes, edges: edges };
    const options = {
        manipulation: {
            enabled: true,
            addNode: false,
            addEdge: function (edgeData, callback) {
                if (edgeData.from !== edgeData.to) {
                    const fromNode = nodes.get(edgeData.from);
                    const toNode = nodes.get(edgeData.to);
                    if (fromNode.type === 'modelium' && toNode.type === 'model' && toNode.parentId === fromNode.id) {
                        edgeData.classes = 'modelium-to-model';
                    }
                    callback(edgeData);
                }
            }
        },
        nodes: {
            shape: 'box',
            size: 30,
            font: { size: 12, color: '#000000' },
            borderWidth: 2,
            shadow: true,
            color: {
                'modelium': {
                    background: '#f1c40f',
                    border: '#f39c12'
                },
                'model': {
                    background: '#3498db',
                    border: '#2980b9'
                },
                'result': {
                    background: '#2ecc71',
                    border: '#27ae60'
                },
                'return': {
                    background: '#27ae60',
                    border: '#1e8449'
                }
            }
        },
        edges: {
            arrows: {
                to: { enabled: true, scaleFactor: 1 },
                middle: { enabled: true, scaleFactor: 0.5 }
            },
            smooth: { type: 'dynamic' },
            color: { color: '#848484', highlight: '#848484', hover: '#848484' },
            width: 2
        },
        physics: { enabled: false },
        interaction: { hover: true }
    };
    network = new vis.Network(container, data, options);

    network.on("click", function (params) {
        if (params.nodes.length > 0) {
            showNodeProperties(params.nodes[0]);
        } else {
            clearProperties();
        }
    });

    setupDragAndDrop();

    network.on("edgeAdded", function (params) {
        // You can add logic here if needed when an edge is added
    });
    network.on("edgeRemoved", function (params) {
        // You can add logic here if needed when an edge is removed
    });
}

// 4. Drag and Drop Setup

function setupDragAndDrop() {
    const container = document.getElementById('modelium-container');
    container.ondragover = function (e) {
        e.preventDefault();
    };
    container.ondrop = function (e) {
        e.preventDefault();
        const type = e.dataTransfer.getData("text");
        const pos = network.DOMtoCanvas({ x: e.clientX, y: e.clientY });
        addNewNode(type, pos.x, pos.y);
    };

    const nodeTypes = document.getElementsByClassName('node-type');
    for (let nodeType of nodeTypes) {
        nodeType.ondragstart = function (e) {
            e.dataTransfer.setData("text", this.dataset.type);
        };
    }
}

// 5. Add New Node

function addNewNode(type, x, y) {
    lastNodeId++;
    let node = {
        id: lastNodeId,
        x: x,
        y: y,
        type: type,
        label: type.charAt(0).toUpperCase() + type.slice(1),
        chainLength: 1,
        loopCount: 0,
        parallelCount: 1,
        hasInterpreter: true,
        model_type: 'Text',
        tools: 'none'
    };

    nodes.add(node);

    if (type === 'modelium') {
        createModeliumStructure(node);
    }

    network.fit();
}

// 6. Create Modelium Structure

function createModeliumStructure(modelium) {
    const baseX = modelium.x;
    const baseY = modelium.y;
    const verticalSpacing = 300;
    const horizontalSpacing = 500;
    const interpreterOffset = 200;


    const childNodes = nodes.get({
        filter: function (node) {
            return node.parentId === modelium.id;
        }
    });
    nodes.remove(childNodes.map(node => node.id));
    edges.remove(edges.getIds({
        filter: function (edge) {
            return childNodes.some(node => node.id === edge.from || node.id === edge.to);
        }
    }));

    for (let p = 0; p < modelium.parallelCount; p++) {
        let currentX = baseX + p * horizontalSpacing;
        let lastResultId, lastInterpreterResultId;

        for (let i = 0; i < modelium.chainLength; i++) {
            let currentY = baseY + (i + 1) * verticalSpacing;

            lastNodeId++;
            const modelNode = {
                id: lastNodeId,
                label: `Model\nType: Text\nTools: all\nFlags: True\nInterpreter: Yes`,
                type: 'model',
                parentId: modelium.id,
                x: currentX,
                y: currentY,
                group: 'model'
            };
            nodes.add(modelNode);

            if (i === 0) {
                edges.add({
                    from: modelium.id,
                    to: modelNode.id,
                    smooth: { type: 'cubicBezier', roundness: 0.2 }
                });
            }

            lastNodeId++;
            const resultNode = {
                id: lastNodeId,
                label: 'Result',
                type: 'result',
                parentId: modelium.id,
                x: currentX - interpreterOffset / 2,
                y: currentY + verticalSpacing / 3,
                group: 'result'
            };
            nodes.add(resultNode);
            edges.add({
                from: modelNode.id,
                to: resultNode.id,
                smooth: { type: 'cubicBezier', roundness: 0.2 }
            });

            lastNodeId++;
            const interpreterNode = {
                id: lastNodeId,
                label: 'Interpreter',
                type: 'interpreter',
                parentId: modelium.id,
                x: currentX + interpreterOffset / 2,
                y: currentY + verticalSpacing / 3,
                group: 'interpreter'
            };
            nodes.add(interpreterNode);

            lastNodeId++;
            const interpreterResultNode = {
                id: lastNodeId,
                label: 'Interpreter Result',
                type: 'result',
                parentId: modelium.id,
                x: currentX + interpreterOffset / 2,
                y: currentY + 2 * (verticalSpacing / 3),
                group: 'result'
            };
            nodes.add(interpreterResultNode);

            edges.add({
                from: resultNode.id,
                to: interpreterNode.id,
                smooth: { type: 'cubicBezier', roundness: 0.2 }
            });
            edges.add({
                from: interpreterNode.id,
                to: interpreterResultNode.id,
                smooth: { type: 'cubicBezier', roundness: 0.2 }
            });

            if (i < modelium.chainLength - 1) {
                edges.add({
                    from: resultNode.id,
                    to: lastNodeId + 1,
                    smooth: { type: 'cubicBezier', roundness: 0.2 }
                });
                edges.add({
                    from: interpreterResultNode.id,
                    to: lastNodeId + 1,
                    smooth: { type: 'cubicBezier', roundness: 0.2 }
                });
            } else if (modelium.loopCount > 0 && i === modelium.chainLength - 1) {

                const firstModelId = modelNode.id - (modelium.chainLength - 1) * 4;

                edges.add({
                    from: resultNode.id,
                    to: firstModelId,
                    smooth: { type: 'cubicBezier', roundness: 0.8 },
                    dashes: [5, 5],
                    color: { color: '#ff0000' },
                    'data-loop-count': modelium.loopCount,
                    label: modelium.loopCount.toString(),
                    class: 'loop-edge'
                });

                edges.add({
                    from: interpreterResultNode.id,
                    to: firstModelId,
                    smooth: { type: 'cubicBezier', roundness: 0.8 },
                    dashes: [5, 5],
                    color: { color: '#ff0000' },
                    'data-loop-count': modelium.loopCount,
                    label: modelium.loopCount.toString(),
                    class: 'loop-edge'
                });
            }

            lastResultId = resultNode.id;
            lastInterpreterResultId = interpreterResultNode.id;
        }


        lastNodeId++;
        const returnNode = {
            id: lastNodeId,
            label: 'Return',
            type: 'return',
            parentId: modelium.id,
            x: currentX,
            y: baseY + (modelium.chainLength + 1) * verticalSpacing,
            group: 'return'
        };
        nodes.add(returnNode);


        edges.add({
            from: lastResultId,
            to: returnNode.id,
            smooth: { type: 'cubicBezier', roundness: 0.2 }
        });
        edges.add({
            from: lastInterpreterResultId,
            to: returnNode.id,
            smooth: { type: 'cubicBezier', roundness: 0.2 }
        });
    }

    network.redraw();
    network.fit();
}

// 7. Node Properties Functions

function clearProperties() {
    document.getElementById('node-properties').innerHTML = '';
}

function showNodeProperties(nodeId) {
    const node = nodes.get(nodeId);
    const propertiesDiv = document.getElementById('node-properties');
    propertiesDiv.innerHTML = `<h3>${node.label} Properties</h3>`;

    if (node.type === 'model') {
        propertiesDiv.innerHTML += `
            <label for="model_type">Model Type:</label><br>
            <select id="model_type">
                ${modelTypes.map(type => `<option value="${type}" ${node.model_type === type ? 'selected' : ''}>${type}</option>`).join('')}
            </select><br>
            <label for="system_instructions">System Instructions:</label><br>
            <textarea id="system_instructions">${node.system_instructions || ''}</textarea><br>
            <label for="prompts">Prompts:</label><br>
            <button id="select-prompts-button" onclick="openPromptSelectionWindow(${nodeId})">Select Prompts</button><br>
            <label for="tools">Tools:</label><br>
            <select id="tools">
                <option value="none" ${node.tools === 'none' ? 'selected' : ''}>None</option>
                <option value="all" ${node.tools === 'all' ? 'selected' : ''}>All</option>
                <option value="chooser" ${node.tools === 'chooser' ? 'selected' : ''}>Chooser</option>
            </select><br>
            <label for="flags">Flags:</label><br>
            <input type="checkbox" id="flags" ${node.flags ? 'checked' : ''}><br>

            <button onclick="updateModelProperties(${nodeId})">Update</button>
        `;
    } else if (node.type === 'modelium') {
        propertiesDiv.innerHTML += `
            <label for="modeliumName">Name:</label><br>
            <input type="text" id="modeliumName" value="${node.label}"><br>
            <label for="chainLength">Chain Length:</label><br>
            <input type="number" id="chainLength" value="${node.chainLength}"><br>
            <label for="loopCount">Loop Count:</label><br>
            <input type="number" id="loopCount" value="${node.loopCount}"><br>
            <label for="parallelCount">Parallel Count:</label><br>
            <input type="number" id="parallelCount" value="${node.parallelCount}"><br>
            <label for="modeliumType">Modelium Type:</label><br>
            <select id="modeliumType">
                <option value="standard" ${node.modeliumType === 'standard' ? 'selected' : ''}>Standard</option>
                <option value="chainLoop" ${node.modeliumType === 'chainLoop' ? 'selected' : ''}>Chain Loop</option>
                </select><br>
            <button onclick="updateModeliumProperties(${nodeId})">Update</button>
        `;
    }
}

// 8. Update Node Properties Functions

function updateModeliumProperties(nodeId) {
    const node = nodes.get(nodeId);
    node.label = document.getElementById('modeliumName').value;
    node.chainLength = parseInt(document.getElementById('chainLength').value);
    node.loopCount = parseInt(document.getElementById('loopCount').value);
    node.parallelCount = parseInt(document.getElementById('parallelCount').value);
    node.modeliumType = document.getElementById('modeliumType').value;
    nodes.update(node);


    const childNodes = nodes.get({
        filter: function (node) {
            return node.parentId === nodeId;
        }
    });
    nodes.remove(childNodes.map(node => node.id));
    edges.remove(edges.getIds({
        filter: function (edge) {
            return childNodes.some(node => node.id === edge.from || node.id === edge.to);
        }
    }));

    createModeliumStructure(node);
}

function updateModelProperties(nodeId) {
    const node = nodes.get(nodeId);
    node.model_type = document.getElementById('model_type').value;
    node.system_instructions = document.getElementById('system_instructions').value;
    node.tools = document.getElementById('tools').value;
    node.flags = document.getElementById('flags').checked;
    const hasInterpreter = document.getElementById('has_interpreter').checked;

    if (hasInterpreter && !node.has_interpreter) {
        addInterpreterNode(node);
        node.has_interpreter = true;
    } else if (!hasInterpreter && node.has_interpreter) {
        removeInterpreterNode(node);
        node.has_interpreter = false;
    }

    nodes.update(node);
    updateModelLabels(node);
}

// 9. Interpreter Node Management

function removeInterpreterNode(modelNode) {
    const connectedEdges = network.getConnectedEdges(modelNode.id);
    const interpreterEdge = edges.get(connectedEdges.find(edgeId => {
        const edge = edges.get(edgeId);
        return edge.from === modelNode.id && nodes.get(edge.to).type === 'interpreter';
    }));

    if (interpreterEdge) {
        const interpreterNode = nodes.get(interpreterEdge.to);
        const interpreterResultEdge = edges.get(network.getConnectedEdges(interpreterNode.id).find(edgeId => {
            const edge = edges.get(edgeId);
            return edge.from === interpreterNode.id && nodes.get(edge.to).type === 'result';
        }));

        if (interpreterResultEdge) {
            nodes.remove(interpreterResultEdge.to);
            edges.remove(interpreterResultEdge.id);
        }

        nodes.remove(interpreterNode.id);
        edges.remove(interpreterEdge.id);
    }
}

function addInterpreterNode(modelNode) {
    lastNodeId++;
    const interpreterNode = {
        id: lastNodeId,
        label: 'Interpreter',
        type: 'interpreter',
        group: 'interpreter',
        x: modelNode.x + 100,
        y: modelNode.y + 50
    };
    nodes.add(interpreterNode);
    edges.add({from: modelNode.id, to: interpreterNode.id});

    lastNodeId++;
    const interpreterResultNode = {
        id: lastNodeId,
        label: 'Interpreter Result',
        type: 'result',
        group: 'result',
        x: interpreterNode.x + 50,
        y: interpreterNode.y + 50
    };
    nodes.add(interpreterResultNode);
    edges.add({from: interpreterNode.id, to: interpreterResultNode.id});
}

// 10. Update Model Labels

function updateModelLabels(node = null) {
    const showModelType = document.getElementById('show-model-type')?.checked || false;
    const showTools = document.getElementById('show-tools')?.checked || false;

    if (!node) {
        const modelNodes = nodes.get({ filter: n => n.type === 'model' });
        modelNodes.forEach(modelNode => {
            updateModelLabels(modelNode);
        });
        return;
    }

    let label = 'Model';
    if (showModelType) label += '\nType: ' + (node.model_type || 'N/A');
    if (showTools) label += '\nTools: ' + (node.tools || 'N/A');
    label += '\nFlags: ' + (node.flags ? 'True' : 'False');
    label += '\nInterpreter: ' + (node.has_interpreter ? 'Yes' : 'No');

    node.label = label;
    nodes.update(node);
}

// 11. Prompt Selection Window

function openPromptSelectionWindow(nodeId) {
    const promptSelectionWindow = document.getElementById('prompt-selection-window');
    promptSelectionWindow.style.display = 'block';


    $('#prompt-tree').jstree({
        'core': {
            'data': promptsData
        }
    });

    promptSelectionWindow.dataset.nodeId = nodeId;
}

function closePromptSelectisonWindow() {
    const promptSelectionWindow = document.getElementById('prompt-selection-window');
    promptSelectionWindow.style.display = 'none';
}

function updatePromptsForModel(nodeId) {
    const modelNode = nodes.get(nodeId);
    const selectedPrompts = $('#prompt-tree').jstree('get_selected');

    modelNode.prompts = selectedPrompts;
    nodes.update(modelNode);

    updateModelLabels(modelNode);
}

// 12. JSON Import/Export Functions

function exportJSON() {
    const jsonData = {
        nodes: nodes.get().map(node => ({
            id: node.id,
            x: node.x,
            y: node.y,
            type: node.type,
            label: node.label,
            chainLength: node.chainLength || undefined,
            loopCount: node.loopCount || undefined,
            parallelCount: node.parallelCount || undefined,
            model_type: node.model_type || undefined,
            system_instructions: node.system_instructions || undefined,
            prompts: node.prompts || undefined,
            tools: node.tools || undefined,
            flags: node.flags || undefined,
            has_interpreter: node.has_interpreter || undefined,
            parentId: node.parentId || undefined
        })),
        edges: edges.get().map(edge => ({
            from: edge.from,
            to: edge.to
        }))
    };

    const jsonString = JSON.stringify(jsonData, null, 2);
    downloadJSON(jsonString, 'modelium.json');
}

function downloadJSON(content, fileName) {
    const a = document.createElement('a');
    const file = new Blob([content], { type: 'text/plain' });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}

function importJSON() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';

    input.onchange = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = (event) => {
            const jsonData = JSON.parse(event.target.result);
            loadJSON(jsonData);
        };
        reader.readAsText(file);
    };

    input.click();
}

function loadJSON(jsonData) {
    nodes.clear();
    edges.clear();
    nodes.add(jsonData.nodes);
    edges.add(jsonData.edges);
    network.fit();
}


// 13. Event Listeners

document.addEventListener('DOMContentLoaded', function () {
    initNetwork();


    const sidebar = document.getElementById('sidebar');

    const importButton = document.createElement('button');
    importButton.textContent = 'Import JSON';
    importButton.addEventListener('click', importJSON);
    sidebar.appendChild(importButton);

    const exportButton = document.createElement('button');
    exportButton.textContent = 'Export JSON';
    exportButton.addEventListener('click', exportJSON);
    sidebar.appendChild(exportButton);
});

document.getElementById('update-prompts-button').addEventListener('click', function() {
    const promptSelectionWindow = document.getElementById('prompt-selection-window');
    const nodeId = promptSelectionWindow.dataset.nodeId;
    updatePromptsForModel(nodeId);
    closePromptSelectisonWindow();
});