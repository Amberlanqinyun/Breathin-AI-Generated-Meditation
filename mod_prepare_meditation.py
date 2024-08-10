from mod_utilize import  app, flash, session, redirect, url_for, render_template, request, datetime, relativedelta
import re

def verify_user_input(user_input):
    # Check if input length is within acceptable range
    min_length = 10
    max_length = 300
    
    if len(user_input) < min_length:
        return False, "It looks like you haven't written much. Could you please share a bit more?"
    elif len(user_input) > max_length:
        return False, f"Your input is quite detailed! Could you try summarizing it to under {max_length} characters?"

    # Simple heuristic to check if the input contains at least one complete sentence
    # A complete sentence here is defined as containing a subject (pronoun/noun) and a verb.
    sentence_regex = r"([A-Z][^.!?]*?[a-z]+[^.!?]*?\.)"
    sentences = re.findall(sentence_regex, user_input)
    
    if len(sentences) == 0:
        return False, "Could you help me understand better by writing a complete thought or sentence?"

    return True, "Thank you for sharing! Your input looks great."

# Example usage
user_input = "Just relaxing with some friends today and feeling a lot of love towards them."
is_valid, message = verify_user_input(user_input)
if is_valid:
    print("Proceed to the next step.")
else:
    print(f"Feedback: {message}")

@app.route('/continue', methods=['POST'])
def continue_page():
    user_input = request.form['user_input']
    is_valid, message = verify_user_input(user_input)
    
    if is_valid:
        # Save the user input to the session or database
        # session['user_input'] = user_input
        return redirect(url_for('prepare_meditation'))
    else:
        # Redirect back to the input page with an error message
        return render_template('input_page.html', error=message)

@app.route('/prepare-meditation')
def prepare_meditation():
    return render_template('prepare_meditation.html')

if __name__ == "__main__":
    app.run(debug=True)