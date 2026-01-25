// Display prediction results on results page
function displayResults() {
  const prediction = JSON.parse(sessionStorage.getItem('prediction')) || {
    riskLevel: 'low',
    confidence: 25
  };
  const patientData = JSON.parse(sessionStorage.getItem('patientData')) || {};

  const riskCard = document.getElementById('riskCard');
  const riskLevel = document.getElementById('riskLevel');
  const riskIcon = document.getElementById('riskIcon');
  const riskDescription = document.getElementById('riskDescription');
  const confidencePercentage = document.getElementById('confidencePercentage');
  const progressFill = document.getElementById('progressFill');
  const recommendationsList = document.getElementById('recommendationsList');
  const patientDataDisplay = document.getElementById('patientDataDisplay');

  // Update risk level and styling
  const riskColors = {
    'low': { bg: 'risk-low', icon: '✓', label: 'Low Risk' },
    'medium': { bg: 'risk-medium', icon: '!', label: 'Moderate Risk' },
    'high': { bg: 'risk-high', icon: '!', label: 'High Risk' }
  };

  const risk = riskColors[prediction.riskLevel] || riskColors.low;
  riskCard.className = 'risk-card ' + risk.bg;
  riskLevel.textContent = risk.label;

  // Update confidence score
  confidencePercentage.textContent = prediction.confidence + '%';
  progressFill.style.width = prediction.confidence + '%';

  // Update description based on risk level
  const descriptions = {
    'low': 'Your cardiovascular metrics indicate a low risk of heart disease. Continue maintaining a healthy lifestyle.',
    'medium': 'Your metrics suggest a moderate risk. Consider consulting with a healthcare provider for preventive measures.',
    'high': 'Your metrics indicate a higher risk. Please schedule a consultation with a cardiologist immediately.'
  };
  riskDescription.textContent = descriptions[prediction.riskLevel] || descriptions.low;

  // Update recommendations based on risk level
  const recommendations = {
    'low': [
      'Maintain your current healthy lifestyle with regular exercise and balanced diet.',
      'Continue monitoring your heart health with regular check-ups annually.',
      'Maintain healthy blood pressure (< 120 mmHg) and cholesterol levels (< 200 mg/dL).',
      'Keep stress levels manageable through relaxation techniques and meditation.',
      'Avoid smoking and limit alcohol consumption.'
    ],
    'medium': [
      'Schedule a consultation with a healthcare provider for preventive measures.',
      'Increase physical activity under professional guidance (150 min/week moderate activity).',
      'Review your diet and reduce salt and saturated fat intake.',
      'Keep stress levels manageable through relaxation techniques.',
      'Monitor blood pressure and cholesterol regularly every 3-6 months.'
    ],
    'high': [
      'Schedule a consultation with a cardiologist immediately for further evaluation.',
      'Consider cardiac stress testing or imaging studies as recommended by your physician.',
      'Begin appropriate medical therapy as prescribed by your healthcare provider.',
      'Follow a heart-healthy diet with reduced sodium and saturated fats.',
      'Monitor vital signs regularly and keep detailed health records.'
    ]
  };

  const recs = recommendations[prediction.riskLevel] || recommendations.low;
  recommendationsList.innerHTML = recs.map(rec => `
    <li>
      <span class="bullet">•</span>
      <span>${rec}</span>
    </li>
  `).join('');

  // Display patient data if available
  if (patientDataDisplay && Object.keys(patientData).length > 0) {
    const dataLabels = {
      age: 'Age (years)',
      sex: 'Sex (0=Female, 1=Male)',
      chestPainType: 'Chest Pain Type (1-4)',
      restingBps: 'Resting BP (mmHg)',
      cholesterol: 'Cholesterol (mg/dL)',
      fastingBloodSugar: 'Fasting Blood Sugar (0 or 1)',
      restingEcg: 'Resting ECG (0-2)',
      maxHeartRate: 'Max Heart Rate (bpm)',
      exerciseAngina: 'Exercise Angina (0=No, 1=Yes)',
      oldpeak: 'ST Depression (Oldpeak)',
      stSlope: 'ST Slope (1-3)'
    };

    const dataHtml = Object.keys(dataLabels)
      .map(key => {
        if (patientData[key] !== undefined) {
          return `
            <div class="data-item">
              <span class="data-label">${dataLabels[key]}:</span>
              <span class="data-value">${patientData[key]}</span>
            </div>
          `;
        }
        return '';
      })
      .join('');

    if (dataHtml) {
      patientDataDisplay.innerHTML = dataHtml;
    }
  }
}