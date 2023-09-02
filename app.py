from flask import Flask, render_template, request
from optimizer import optimizer

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

@app.route('/nba', methods=['GET', 'POST'])
def nba():
    if request.method == 'POST':
        team1 = request.form.get('input1')
        team2 = request.form.get('input2')
        risklv = request.form.get('risklv')

        if team1 and team2 and risklv: 
            try:
                if risklv == 'risk':
                    result = optimizer('nba', team1, team2, 'risk')
                elif risklv == 'safe':
                    result = optimizer('nba', team1, team2, 'safe')

                return render_template('nba.html', result=result)
            except Exception as e:
                error_message = f"Error occurred: {str(e)}"
                return render_template('nba.html', error=error_message)
    return render_template('nba.html')

@app.route('/wnba', methods=['GET', 'POST'])
def wnba():
    if request.method == 'POST':
        team1 = request.form.get('input1')
        team2 = request.form.get('input2')
        risklv = request.form.get('risklv')

        if team1 and team2:  # Check if both inputs are filled
            print(team1, team2, risklv)
            try:
                if risklv == 'risk':
                    result = optimizer('wnba', team1, team2, 'risk')
                elif risklv == 'safe':
                    result = optimizer('wnba', team1, team2, 'safe')

                # Return the result to be displayed in the HTML template
                return render_template('wnba.html', result=result)
            except Exception as e:
                error_message = f"Error occurred: {str(e)}"
                return render_template('main.html', error=error_message)
    return render_template('wnba.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
