from flask import Flask, render_template, request, session, redirect, url_for
from blackjack_logic import deal_card, calculate_score, determine_result
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generated once at startup
app.secret_key = "your_secret_key"
@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize on first visit
    if request.method == "GET":
        # Only clear on page refresh, not on form submissions
        session.clear()
        session['player_hand'] = []
        session['dealer_hand'] = []
        session['player_score'] = 0
        session['dealer_score'] = 0
        session['game_over'] = False
        session['result'] = "Welcome to Blackjack! Click 'Start' to begin."
    
    if request.method == "POST":
        move = request.form.get("move")
        
        if move == "start":
            session['player_hand'] = [deal_card(), deal_card()]
            session['dealer_hand'] = [deal_card(), deal_card()]
            session['player_score'] = calculate_score(session['player_hand'])
            session['dealer_score'] = calculate_score(session['dealer_hand'])
            session['game_over'] = False
            session['result'] = "Game started! Your turn."
        
        elif move == "hit" and not session['game_over']:
            session['player_hand'].append(deal_card())
            session['player_score'] = calculate_score(session['player_hand'])
            
            if session['player_score'] > 21:
                session['result'] = f"Your hand: {session['player_score']}. Bust! You lost."
                session['game_over'] = True
            else:
                session['result'] = f"Your hand: {session['player_score']}. Your turn."
        
        elif move == "stand" and not session['game_over']:
            while session['dealer_score'] < 17:
                session['dealer_hand'].append(deal_card())
                session['dealer_score'] = calculate_score(session['dealer_hand'])
                
            session['result'] = determine_result(session['player_score'], session['dealer_score'])
            session['game_over'] = True
        # In your POST handler
        elif move == "exit":
            session.clear()
            session['result'] = "Welcome to Blackjack! Click 'Start' to begin."
            return redirect(url_for('index'))
    return render_template(
      "index.html",
      player_hand=session['player_hand'],
      dealer_first_card=session['dealer_hand'][0] if session['dealer_hand'] else None,
      dealer_hand=session['dealer_hand'] if session['game_over'] else None,
      player_score=session['player_score'],
      dealer_score=session['dealer_score'] if session['game_over'] else None,
      result=session['result'],
      game_over=session['game_over']
)

if __name__ == "__main__":
    app.run(debug=True)