document.addEventListener("DOMContentLoaded", function() {
    const panels = document.getElementsByClassName("panel-calculator");
    const previousButton = document.getElementById("previous-button");
    const nextButton = document.getElementById("next-button");
    let currentPanelIndex = 0;

    function showPanel(index) {
      for (let i = 0; i < panels.length; i++) {
        if (i === index) {
          panels[i].classList.add("active");
        } else {
          panels[i].classList.remove("active");
        }
      }
      previousButton.disabled = index === 0;
      nextButton.disabled = index === panels.length - 1;
    }

    function goToPreviousPanel() {
      if (currentPanelIndex > 0) {
        currentPanelIndex--;
        showPanel(currentPanelIndex);
      }
    }

    function goToNextPanel() {
      if (currentPanelIndex < panels.length - 1) {
        currentPanelIndex++;
        showPanel(currentPanelIndex);
      }
    }

    previousButton.addEventListener("click", goToPreviousPanel);
    nextButton.addEventListener("click", goToNextPanel);

    showPanel(currentPanelIndex);
  });