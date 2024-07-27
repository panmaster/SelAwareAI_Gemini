'use strict';

let nodes = new vis.DataSet([]);
let edges = new vis.DataSet([]);
let network = null;
let lastNodeId = 0;

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
        adjustModeliumStructure();
    });
    network.on("edgeRemoved", function (params) {
        adjustModeliumStructure();
    });
}

function setupDragAndDrop() {
    const container = document.getElementById('modelium-container');
    container.ondragover = function (e) { e.preventDefault(); };
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

function addNewNode(type, x, y) {
    lastNodeId++;
    let node = {
        id: lastNodeId,
        x: x,
        y: y,
        type: type,
        label: type.charAt(0).toUpperCase() + type.slice(1)
    };

    nodes.add(node);

    if (type === 'modelium') {
        createModeliumStructure(node);
    }

    network.fit(); // Adjust view after adding new nodes
}



function createModeliumStructure(modelium) {
    const baseX = modelium.x;
    const baseY = modelium.y;
    const verticalSpacing = 80;
    const horizontalOffset = 100;

    // Create Model node
    lastNodeId++;
    const modelNode = {
        id: lastNodeId,
        label: 'Model\nType: Text\nTools: all\nFlags: True\nInterpreter: Yes',
        type: 'model',
        parentId: modelium.id,
        x: baseX,
        y: baseY + verticalSpacing,
        group: 'model'
    };
    nodes.add(modelNode);

    // Create Result node
    lastNodeId++;
    const resultNode = {
        id: lastNodeId,
        label: 'Result',
        type: 'result',
        parentId: modelium.id,
        x: baseX,
        y: baseY + verticalSpacing * 2,
        group: 'result'
    };
    nodes.add(resultNode);

    // Create Interpreter node
    lastNodeId++;
    const interpreterNode = {
        id: lastNodeId,
        label: 'Interpreter',
        type: 'interpreter',
        parentId: modelium.id,
        x: baseX - horizontalOffset,
        y: baseY + verticalSpacing * 3,
        group: 'interpreter'
    };
    nodes.add(interpreterNode);

    // Create Interpreter Result node
    lastNodeId++;
    const interpreterResultNode = {
        id: lastNodeId,
        label: 'Interpreter Result',
        type: 'result',
        parentId: modelium.id,
        x: baseX - horizontalOffset,
        y: baseY + verticalSpacing * 4,
        group: 'result'
    };
    nodes.add(interpreterResultNode);

    // Create Return node
    lastNodeId++;
    const returnNode = {
        id: lastNodeId,
        label: 'Return',
        type: 'return',
        parentId: modelium.id,
        x: baseX,
        y: baseY + verticalSpacing * 5,
        group: 'return'
    };
    nodes.add(returnNode);

    // Add edges with curved arrows
    edges.add([
        {from: modelium.id, to: modelNode.id, smooth: {type: 'cubicBezier'}},
        {from: modelNode.id, to: resultNode.id, smooth: {type: 'cubicBezier'}},
        {from: resultNode.id, to: interpreterNode.id, smooth: {type: 'cubicBezier', roundness: 0.5}},
        {from: interpreterNode.id, to: interpreterResultNode.id, smooth: {type: 'cubicBezier'}},
        {from: resultNode.id, to: returnNode.id, smooth: {type: 'cubicBezier', roundness: -0.2}},
        {from: interpreterResultNode.id, to: returnNode.id, smooth: {type: 'cubicBezier', roundness: 0.5}}
    ]);

    network.fit();
}

function generateStructuredDescription(modelium) {
    let schema = {
        type: modelium.modeliumType,
        name: modelium.label,
        chainLength: modelium.chainLength,
        parallelCount: modelium.parallelCount,
        loopCount: modelium.loopCount,
        models: [],
        results: [],
        returns: [],
        nestedModeliums: []
    };

    const childNodes = nodes.get({
        filter: function (node) {
            return node.parentId === modelium.id;
        }
    });

    childNodes.forEach(node => {
        switch (node.type) {
            case 'model':
                schema.models.push({
                    id: node.id,
                    systemInstructions: node.system_instructions,
                    prompts: node.prompts,
                    modelType: node.model_type,
                    tools: node.tools
                });
                break;
            case 'result':
                schema.results.push({ id: node.id });
                break;
            case 'return':
                schema.returns.push({ id: node.id });
                break;
            case 'modelium':
                schema.nestedModeliums.push(generateStructuredDescription(node));
                break;
        }
    });

    return schema;
}

function generateAndDisplayStructuredDescription() {
    const modeliumNodes = nodes.get({
        filter: function (node) {
            return node.type === 'modelium';
        }
    });

    if (modeliumNodes.length === 0) {
        alert('No Modelium node found!');
        return;
    }

    const rootModelium = modeliumNodes.reduce((prev, current) =>
        (prev.y < current.y) ? prev : current
    );

    const structuredDescription = generateStructuredDescription(rootModelium);
    document.getElementById('structureDescription').value = JSON.stringify(structuredDescription, null, 2);
}

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
            <label for="tools">Tools:</label><br>
            <select id="tools">
                <option value="none" ${node.tools === 'none' ? 'selected' : ''}>None</option>
                <option value="all" ${node.tools === 'all' ? 'selected' : ''}>All</option>
                <option value="chooser" ${node.tools === 'chooser' ? 'selected' : ''}>Chooser</option>
            </select><br>
            <label for="flags">Flags:</label><br>
            <input type="checkbox" id="flags" ${node.flags ? 'checked' : ''}><br>
            <label for="has_interpreter">Has Interpreter:</label><br>
            <input type="checkbox" id="has_interpreter" ${node.has_interpreter ? 'checked' : ''}><br>
            <button onclick="updateModelProperties(${nodeId})">Update</button>
        `;
    }
    // Add properties for other node types as needed
}

function updateModeliumProperties(nodeId) {
    const node = nodes.get(nodeId);
    node.label = document.getElementById('modeliumName').value;
    node.chainLength = parseInt(document.getElementById('chainLength').value);
    node.loopCount = parseInt(document.getElementById('loopCount').value);
    node.parallelCount = parseInt(document.getElementById('parallelCount').value);
    node.modeliumType = document.getElementById('modeliumType').value;
    nodes.update(node);

    // Remove existing child nodes and edges
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

// Function to adjust the Modelium structure for better visualization
function adjustModeliumStructure() {
    const allNodes = nodes.get();
    let maxX = 0;
    allNodes.forEach(node => {
        if (node.x > maxX) {
            maxX = node.x;
        }
    });
    allNodes.forEach(node => {
        node.x = maxX + 100;
        nodes.update(node);
    });
}

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


function updateModelLabels(node = null) {
    const showPrompt = document.getElementById('show-prompt').checked;
    const showSystemInstructions = document.getElementById('show-system-instructions').checked;
    const showTools = document.getElementById('show-tools').checked;
    const showModelType = document.getElementById('show-model-type').checked;

    if (!node) {
        const modelNodes = nodes.get({ filter: n => n.type === 'model' });
        modelNodes.forEach(modelNode => {
            updateModelLabels(modelNode);
        });
        return;
    }

    let label = 'Model';
    if (showPrompt) label += '\nPrompt: ' + (node.prompts || 'N/A');
    if (showSystemInstructions) label += '\nSys Instr: ' + (node.system_instructions || 'N/A');
    if (showTools) label += '\nTools: ' + (node.tools || 'N/A');
    if (showModelType) label += '\nType: ' + (node.model_type || 'N/A');

    node.label = label;
    nodes.update(node);
}

function addResultNode(modelNode) {
    lastNodeId++;
    const resultNode = {
        id: lastNodeId,
        label: 'Result',
        type: 'result',
        group: 'result',
        x: modelNode.x + 50,
        y: modelNode.y + 50
    };
    nodes.add(resultNode);
    edges.add({from: modelNode.id, to: resultNode.id});
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
initNetwork();