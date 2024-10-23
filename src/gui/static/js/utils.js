// JavaScript to handle row selection

function selectCheckboxesAction(selected = true, cls = "") {
    if (cls === "") {
        console.error("No class provided for row selection");
        return;
    }
    const rowCheckboxes = document.querySelectorAll("." + cls);
    rowCheckboxes.forEach(checkbox => {
        checkbox.checked = selected;
    });
}

function getSelectedSamples(cls = "") {
    if (cls === "") {
        console.error("No class provided for row selection");
        return;
    }
    const rowCheckboxes = document.querySelectorAll("." + cls);
    const selectedSampleIds = [];
    rowCheckboxes.forEach(checkbox => {
        if (checkbox.checked) {
            selectedSampleIds.push(Number(checkbox.attributes['sample-id'].value));
        }
    });
    return selectedSampleIds;
}

function downloadFile(filename, contentB64String) {
    console.log("Downloading file " + filename);
    // prepare the data
    const byteCharacters = atob(contentB64String);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });

    // download
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();

    // cleanup
    document.body.removeChild(link);
    window.URL.revokeObjectURL(link.href);
}