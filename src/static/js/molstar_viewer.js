// Function to initialize the Mol* Viewer
function initializeMolstarViewer(containerId, structureUrl) {
    if (!structureUrl) {
        console.error("No structure URL provided");
        return;
    }

    // Initialize Mol* Viewer using the correct constructor
    const viewer = new Molstar.Viewer(containerId, {
        layoutIsExpanded: true,
        layoutShowControls: true,
        layoutShowSequence: true,
        layoutShowLog: false,
        layoutShowLeftPanel: false
    });

    // Load the PDB file from the provided URL
    viewer.loadStructureFromUrl(structureUrl, 'mmcif')
        .catch(err => console.error("Error loading structure:", err));
}

// Function to initialize the viewer on page load
export function initViewerOnLoad(structureUrl) {
    if (structureUrl) {
        initializeMolstarViewer('molstar-container', structureUrl);
    } else {
        console.error("Structure URL is not defined");
    }
}
