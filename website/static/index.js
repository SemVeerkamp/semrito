function deletePrediction(predictionId) {
  fetch("/delete-prediction", {
    method: "POST",
    body: JSON.stringify({ predictionId: predictionId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
