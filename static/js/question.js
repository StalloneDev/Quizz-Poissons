let timeRemaining = 15; // Temps de départ (en secondes)
let timer; // Variable globale pour le timer
let totalElapsedTime = 0; // Variable pour le temps total écoulé
let startTime; // Heure de départ pour chaque question
let timeoutCount = 0;

// Fonction pour afficher le popup de temps Ecoule
let timeoutPopup = document.getElementById('timeout-popup'); 



function startTimer() {
    let timeLeft = timeRemaining;

    startTime = new Date();

    const timerElement = document.getElementById('time-remaining');
    const circle = document.querySelector('#timer circle');
    const circumference = 2 * Math.PI * 18;
    circle.style.strokeDasharray = circumference;

    timer = setInterval(() => {
        console.log(`Temps restant : ${timeLeft}`); // Journal pour voir le temps restant
        if (timeLeft > 0) {
            timeLeft--;
            timerElement.textContent = timeLeft;
            const dashoffset = circumference * (1 - timeLeft / timeRemaining);
            circle.style.strokeDashoffset = dashoffset;
        } else {
            clearInterval(timer);
            console.log("Le temps est écoulé."); // Journal pour vérifier si le temps atteint zéro
            console.log(`TimeoutCount avant incrément : ${timeoutCount}`); // Journal pour vérifier timeoutCount avant incrément
            handleTimeout(); // Appel à handleTimeout pour gérer la fin du temps
        }
    }, 1000);
}

function handleTimeout() {
    timeoutCount++;
    console.log(`TimeoutCount après incrément dans handleTimeout : ${timeoutCount}`); // Journal pour vérifier timeoutCount après incrément
    recordElapsedTime(); // Enregistre le temps écoulé pour cette question

    if (timeoutCount < 2) {
        showTimeoutPopup(false); // Premier échec
    } else {
        showTimeoutPopup(true); // Deuxième échec - passe à la question suivante
    }
}

// Fonction pour afficher le popup de temps Ecoule
function showTimeoutPopup(isSecondTimeout) {
    console.log(`Appel de showTimeoutPopup avec isSecondTimeout = ${isSecondTimeout}`);
    console.log(`TimeoutCount dans showTimeoutPopup : ${timeoutCount}`); // Journal pour vérifier timeoutCount
    timeoutPopup.style.display = 'block';

    if (!isSecondTimeout) {
        document.getElementById('popup-message-1').style.display = 'block';
        document.getElementById('popup-message-2').style.display = 'none';
        document.getElementById('popup-close-btn').onclick = function() {
            console.log("Fermeture du popup pour premier échec.");
            timeoutPopup.style.display = 'none';
            resetTimer(); // Redémarre le timer pour le second essai
        };
    } else {
        document.getElementById('popup-message-1').style.display = 'none';
        document.getElementById('popup-message-2').style.display = 'block';
        document.getElementById('popup-close-btn').onclick = function() {
            console.log("Fermeture du popup pour deuxième échec, passage à la question suivante.");
            showNextQuestion(); // Passe à la question suivante
        };
    }
}

function recordElapsedTime() {
    let endTime = new Date(); // Heure de fin de la question
    let elapsedTime = (endTime - startTime) / 1000; // Temps écoulé en secondes
    totalElapsedTime += elapsedTime; // Ajoute le temps de cette question au total
    console.log(`Temps total écoulé jusqu'à présent : ${totalElapsedTime} secondes`);
}

function showNextQuestion() {
    recordElapsedTime(); // Enregistre le temps écoulé pour cette question
    clearInterval(timer);
    console.log(`TimeoutCount dans showNextQuestion avant redirection : ${timeoutCount}`); // Journal pour vérifier timeoutCount
    let currentQuestionId = parseInt(document.getElementById('game-container').dataset.currentQuestion);
    let nextQuestionId = currentQuestionId + 1;

    window.location.href = `/question/${nextQuestionId}/`;
}

// Option de sélection pour faire le choix
let selectedOption = null; // Variable pour suivre l'option sélectionnée

function selectOption(optionElement) {
    if (selectedOption) {
        selectedOption.classList.remove('selected');
    }

    optionElement.classList.add('selected');
    selectedOption = optionElement;

    const selectedOptionValue = optionElement.getAttribute('data-option');
    document.getElementById('selected-option').value = selectedOptionValue;

    // Marque la question comme répondue et arrête le timer, mais ne passe pas à la question suivante
    //isAnswered = true;
    //recordElapsedTime(); // Enregistre le temps écoulé pour cette question
    //clearInterval(timer);
    //console.log("Réponse sélectionnée, timer arrêté."); // Journal pour confirmer l'arrêt du timer
}

function resetTimer() {
    clearInterval(timer);
    startTimer();
}

// Démarre le timer au début
startTimer();


function closePopup() {
    document.getElementById('wrong-answer-popup').style.display = 'none';
}