from django.shortcuts import render, redirect
import random

# Structure des questions
questions = [
    {
        'id': 1,
        'question': "Quel poisson anime les récifs dès 3 m de profondeur ?",
        'options': ['Chirurgien.jpg', 'Coffre-Mouton.jpg', 'Pyjama.jpg', 'Pastenagues.jpg'],
        'correct': 'Chirurgien.jpg',
        'info': {
            'nom': "Chirurgien Bleu",
            'description': "Au stade juvénile, il est entièrement jaune vif. Une forme intermédiaire adopte déjà la couleur bleue sur tout le corps, mais conserve la nageoire caudale jaune. Les adultes sont entièrement bleus."
        }
    },
    {
        'id': 2,
        'question': "Quel poisson possède deux épines venimeuses et vit sur les fonds sableux ?",
        'options': ['Pastenagues.jpg', 'Thazard-Maquereau.jpg', 'Coffre-Mouton.jpg', 'Fee-Lorette.jpg'],
        'correct': 'Pastenagues.jpg',
        'info': {
            'nom': "Pastenague Américaine",
            'description': "Cette raie utilise son aiguillon venimeux pour se défendre, mais elle est généralement inoffensive si elle n’est pas dérangée."
        }
    },
    {
        'id': 3,
        'question': "Quel poisson se nourrit de coraux et vit en couple ?",
        'options': ['Pyjama.jpg', 'Chirurgien.jpg', 'Coffre-Mouton.jpg', 'Fee-Lorette.jpg'],
        'correct': 'Pyjama.jpg',
        'info': {
            'nom': "Papillon Pyjama",

            'description': "Ce poisson est de forme caractéristique en ailes de papillon. Il est rayé de blanc et noir verticalement et ses nageoires sont noires. Au stade juvénile, il possède une tache noire cerclée de blanc à l’arrière de la dorsale."
            
        }
    },
    {
        'id': 4,
        'question': "Quel poisson se nourrit aussi bien en pleine eau que sur les fonds ?",
        'options': ['Sergent-Major.jpg', 'Thazard-Maquereau.jpg', 'Baracuda.jpg', 'Coffre-Mouton.jpg'],
        'correct': 'Sergent-Major.jpg',
        'info': {
            'nom': "Sergent Major",
            'description': "Ce poisson est très caractéristique avec ses bandes verticales noires sur fond jaune. Il peut adopter une phase sombre où l’ensemble du corps est gris foncé. Attention à ne pas le confondre avec le Sergent de Nuit !"
            
        }
    },
    {
        'id': 5,
        'question': "Quel prédateur a des dents acérées et peut atteindre 1,20 m de longueur ?",
        'options': ['Pastenagues.jpg', 'Thazard-Maquereau.jpg', 'Pyjama.jpg', 'Coffre-Mouton.jpg'],
        'correct': 'Thazard-Maquereau.jpg',
        'info': {
            'nom': "Thazard Maquereau",
            'description': "Ce poisson est le plus commun des thazards. Il rôde souvent à quelques mètres au-dessus des fonds coralliens."
        }
    },
    {
        'id': 6,
        'question': "Quel petit poisson est souvent caché dans les anfractuosités des récifs coralliens et ne sort qu’à la nuit tombée ?",
        'options': ['Cardinal-Longues-Epines.jpg', 'Chirurgien.jpg', 'Baracuda.jpg', 'Coffre-Mouton.jpg'],
        'correct': 'Cardinal-Longues-Epines.jpg',
        'info': {
            'nom': "Cardinal Longue Epine",
            'description': "Il est de la famille des Poissons-soldats. Il a un museau pointu avec la mâchoire inférieure se projetant vers l’avant. Il a une épine impressionnante. Il vit parfois en groupe très dense."
            
        }
    },
    {
        'id': 6,
        'question': "Quel petit poisson est souvent caché dans les anfractuosités des récifs coralliens et ne sort qu’à la nuit tombée ?",
        'options': ['Cardinal-Longues-Epines.jpg', 'Chirurgien.jpg', 'Baracuda.jpg', 'Coffre-Mouton.jpg'],
        'correct': 'Cardinal-Longues-Epines.jpg',
        'info': {
            'nom': "Cardinal Longue Epine",
            'description': "Il est de la famille des Poissons-soldats. Il a un museau pointu avec la mâchoire inférieure se projetant vers l’avant. Il a une épine impressionnante. Il vit parfois en groupe très dense."
            
        }
    },
    
]

def index(request):
    request.session['score'] = 0
    return render(request, 'quiz/index.html')

def question(request, question_id):
    # Vérifier si la question existe
    if question_id > len(questions):
        return redirect('end_quiz', score=request.session.get('score', 0))

    question_data = questions[question_id - 1]
    random.shuffle(question_data['options'])
    selected_option = request.POST.get('selected_option')
    correct = selected_option == question_data['correct']

    # Mettre à jour le score si la réponse est correcte
    if correct:
        request.session['score'] += 1

    next_question = question_id + 1 if question_id < len(questions) else None

    # Rediriger vers la question suivante ou vers la fin
    if next_question is None:
        return redirect('end_quiz', score=request.session['score'], question_id=question_id)

    return render(request, 'quiz/question.html', {
        'question': question_data,
        'total_questions': len(questions),
        'score': request.session['score'],
        'next_question': next_question
    })


def result(request, question_id):
    selected_option = request.POST.get('selected_option')
    question_data = questions[question_id - 1]
    correct = selected_option == question_data['correct']
    
    # Initialiser ou récupérer le nombre de tentatives restantes
    attempt_left = request.session.get('attempts', 2)

    if correct:
        request.session['score'] = request.session.get('score', 0) + 1
        attempt_left = 2  # Réinitialiser les tentatives pour la prochaine question
    else:
        attempt_left -= 1

    # Mettre à jour le nombre de tentatives dans la session
    request.session['attempts'] = attempt_left

    # Déterminer la question suivante ou la fin du quiz
    next_question = question_id + 1 if question_id < len(questions) else None

    # Si le joueur échoue deux fois (tentatives restantes = 0), afficher le message d'échec et les infos
    if attempt_left == 0:
        request.session['attempts'] = 2  # Réinitialiser pour la prochaine question
        return render(request, 'quiz/result.html', {
            'question': question_data,
            'correct': False,
            'selected_option': selected_option,
            'info': question_data['info'],  # Afficher les infos sur la bonne réponse
            'next_question': next_question,
            'score': request.session['score'],
            'total_questions': len(questions),
            'attempt_left': attempt_left,
        })

    # Si c'était la dernière question, rediriger vers la fin du quiz
    if next_question is None:
        score = request.session['score']
        return redirect('end_quiz', score=score, question_id=question_id)

    # Afficher la page de résultat standard si la tentative est valide
    return render(request, 'quiz/result.html', {
        'question': question_data,
        'correct': correct,
        'selected_option': selected_option,
        'info': question_data['info'] if correct else None,
        'next_question': next_question,
        'score': request.session['score'],
        'total_questions': len(questions),
        'attempt_left': attempt_left,
    })

def end_quiz(request, score, question_id):
    # Calcul du total des points (une bonne réponse = 5 points)
    question_data = questions[question_id - 1]
    score_final = score * 5

    # Détermination du trophée à afficher
    if score >= 6:
        trophée = 'or'
    elif 5 <= score <= 5:
        trophée = 'argent'
    elif 2 <= score <= 3:
        trophée = 'bronze'
    else:
        trophée = 'emogie'

    return render(request, 'quiz/end.html', {
        'score': score,
        'score_final': score_final,
        'trophée': trophée,
        'question': question_data,
        'total_questions': len(questions),
    })



