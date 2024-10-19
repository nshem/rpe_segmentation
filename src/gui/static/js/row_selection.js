// JavaScript to handle row selection

function selectCheckboxesAction(selected = true, cls = "") {
    if (cls === "") {
        console.error("No class provided for row selection");
        return;
    }
    const rowCheckboxes = document.querySelectorAll("." + cls);
    console.log(rowCheckboxes);
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