from django.shortcuts import render
from django.contrib.auth.models import User
from dotenv import load_dotenv
import google.generativeai as genai
import os
import pickle
import numpy as np
import re


ml_model = pickle.load(open("./mental_health_prediction.sav",'rb'))

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)


load_dotenv()
os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')


# Create your views here.

def Home(request):
    return render (request,'baseApp/index.html')





def find_all_and_replace(text, sub):
  """
  Finds all occurrences of a substring and replaces them with an empty string.

  Args:
      text: The string to search.
      sub: The substring to replace.

  Returns:
      The modified string with all occurrences of 'sub' replaced.
  """
  new_text = text
  start = 0
  while True:
    # Find the next occurrence
    found = new_text.find(sub, start)
    if found == -1:
      break
    # Replace the occurrence and update starting position
    new_text = new_text[:found] + new_text[found+len(sub):]
    start = found
  return new_text



videos = {
    0: {
        "https://youtu.be/z-IR48Mb3W0?si=5V8YxrbxuXTcN3Se": "https://img.youtube.com/vi/z-IR48Mb3W0/0.jpg",
        "https://youtu.be/Fm73eVoi4dw?si=yiRGIfOsi4VIrYpp": "https://img.youtube.com/vi/Fm73eVoi4dw/0.jpg",
        "https://youtu.be/BZOLxSQwER8?si=vUNztWxoFUPzw6ey": "https://img.youtube.com/vi/BZOLxSQwER8/0.jpg",
        # "https://youtu.be/OzO8EAOEGJ8?si=Oi_oMnBGtPlhIJFR": "https://img.youtube.com/vi/OzO8EAOEGJ8/0.jpg",
        # "https://youtu.be/MZ5r99SBLrs?si=dT5TX5Yme2Mlt3de": "https://img.youtube.com/vi/MZ5r99SBLrs/0.jpg",

    },
    1: {
        "https://youtu.be/9mPwQTiMSj8?si=tkaZ40cu20cLtjNu": "https://img.youtube.com/vi/9mPwQTiMSj8/0.jpg",
        "https://youtu.be/JOKS9Bx8-Sw?si=s_paZtpEv8ERHnlO": "https://img.youtube.com/vi/JOKS9Bx8/0.jpg",
        "https://youtu.be/BVJkf8IuRjE?si=moZNs1ow-k7tLsNz": "https://img.youtube.com/vi/BVJkf8IuRjE/0.jpg",
        # "https://youtu.be/zTuX_ShUrw0?si=7pJx_dcU3IEoKnMm": "https://img.youtube.com/vi/zTuX_ShUrw0/0.jpg",
        # "https://youtu.be/vtUdHOx494E?si=cMhLCCbPolitlF1u": "https://img.youtube.com/vi/vtUdHOx494E/0.jpg",

    },
    2: {
        "https://youtu.be/z-IR48Mb3W0?si=5V8YxrbxuXTcN3Se": "https://img.youtube.com/vi/z-IR48Mb3W0/0.jpg",
        "https://youtu.be/Fm73eVoi4dw?si=yiRGIfOsi4VIrYpp": "https://img.youtube.com/vi/Fm73eVoi4dw/0.jpg",
        "https://youtu.be/BZOLxSQwER8?si=vUNztWxoFUPzw6ey": "https://img.youtube.com/vi/BZOLxSQwER8/0.jpg",
        # "https://youtu.be/OzO8EAOEGJ8?si=Oi_oMnBGtPlhIJFR": "https://img.youtube.com/vi/OzO8EAOEGJ8/0.jpg",
        # "https://youtu.be/MZ5r99SBLrs?si=dT5TX5Yme2Mlt3de": "https://img.youtube.com/vi/MZ5r99SBLrs/0.jpg",

    },
    3: {
        "https://youtu.be/1BBiaxOxXas?si=lVXUCIqY7N5NjpFN": "https://img.youtube.com/vi/1BBiaxOxXas/0.jpg",
        "https://youtu.be/1BBiaxOxXas?si=j9gatadXIKovNBSH": "https://img.youtube.com/vi/1BBiaxOxXas/0.jpg",
        "https://youtu.be/QFt_5kSUQyM?si=1twlenCwPjN-2ocC": "https://img.youtube.com/vi/QFt_5kSUQyM/0.jpg",
        # "https://youtu.be/2KXtlIX_yUs?si=SE4RS5y7xjoYgp85": "https://img.youtube.com/vi/2KXtlIX_yUs/0.jpg",
        # "https://youtu.be/aAvZPaDlwR0?si=WTc4o6bcdIl9mTrv": "https://img.youtube.com/vi/aAvZPaDlwR0/0.jpg",

    },
    4: {
        "https://youtu.be/n3Xv_g3g-mA?si=cfU5SLQnIEPtIo-E": "https://img.youtube.com/vi/n3Xv_g3g-mA/0.jpg",
        "https://youtu.be/JxbYPk1MIyw?si=tujk_3eTEHw1a9Mh": "https://img.youtube.com/vi/JxbYPk1MIyw/0.jpg",
        "https://youtu.be/TWNL7EClClo?si=Hao7pDbhBrrWqg2e": "https://img.youtube.com/vi/TWNL7EClClo/0.jpg",
        # "https://youtu.be/dWS3A2EAwTk?si=Kc2XICKov-MdgR-m": "https://img.youtube.com/vi/dWS3A2EAwTk/0.jpg",
        # "https://youtu.be/GdcDKpLUajs?si=GNXZWE7bZqNJVMi9": "https://img.youtube.com/vi/GdcDKpLUajs/0.jpg",

    },
   
}
 



def Test(request):

    context = {}
      # ... (existing code to collect form data)
    if request.method == 'POST':
        # Extract the form data from the POST request
        feeling_nervous = request.POST.get('feeling_nervous')
        panic = request.POST.get('panic') 
        breathing_rapidly = request.POST.get('breathing_rapidly') 
        sweating = request.POST.get('sweating') 
        trouble_in_concentration = request.POST.get('trouble_in_concentration') 
        having_trouble_in_sleeping = request.POST.get('having_trouble_in_sleeping') 
        having_trouble_with_work = request.POST.get('having_trouble_with_work') 
        hopelessness = request.POST.get('hopelessness') 
        anger = request.POST.get('anger') 
        over_react = request.POST.get('over_react') 
        change_in_eating = request.POST.get('change_in_eating') 
        suicidal_thought = request.POST.get('suicidal_thought') 
        feeling_tired = request.POST.get('feeling_tired') 
        close_friend = request.POST.get('close_friend') 
        social_media_addiction = request.POST.get('social_media_addiction') 
        weight_gain = request.POST.get('weight_gain') 
        material_possessions = request.POST.get('material_possessions') 
        introvert = request.POST.get('introvert') 
        popping_up_stressful_memory = request.POST.get('popping_up_stressful_memory') 
        having_nightmares = request.POST.get('having_nightmares') 
        avoids_people_or_activities = request.POST.get('avoids_people_or_activities') 
        feeling_negative = request.POST.get('feeling_negative') 
        trouble_concentrating = request.POST.get('trouble_concentrating') 
        blamming_yourself = request.POST.get('blamming_yourself') 

        # Prediction Logic (replace with your actual model)

        input_tuple = (feeling_nervous,panic,breathing_rapidly,sweating,trouble_in_concentration, 
                 having_trouble_in_sleeping,having_trouble_with_work,hopelessness,anger,over_react,change_in_eating,suicidal_thought,feeling_tired,close_friend,social_media_addiction,weight_gain,material_possessions,introvert,popping_up_stressful_memory,having_nightmares,avoids_people_or_activities,feeling_negative,trouble_concentrating,blamming_yourself)

        print(input_tuple)
        input_array = np.array(input_tuple)
        input_reshaped = input_array.reshape(1, -1)
        scaled_input = scaler.transform(input_reshaped)
        prediction = ml_model.predict(scaled_input)
        print(prediction)

        # Mental health conditions and descriptions dictionary
        conditions = {
            0: {"issue": "no issues", "description": "The user is fine."},
            1: {"issue": "Anxiety", "description": "Feeling nervous, restless, or having trouble concentrating. You might also have physical symptoms like rapid heartbeat, sweating, or trouble sleeping."},
            2: {"issue": "Depression", "description": "Feeling hopeless, sad, or losing interest in activities you used to enjoy. You might also have changes in sleep or appetite."},
            3: {"issue": "Stress", "description": "Feeling overwhelmed, anxious, or irritable. Stress can also cause physical symptoms like headaches, muscle tension, or fatigue."},
            4: {"issue": "Loneliness", "description": "Feeling isolated or alone, even when you're around other people."},
            
        }

        # Access data based on prediction
        current_issue = conditions.get(prediction[0])
        print("current_issue", current_issue)

        if prediction[0] == 0:
            prompt = f"The User is completely normal. Just provide some more self care tips."
        else:
            prompt = f"Write a supportive and informative message about {current_issue['issue']}. Include information on what it is, symptoms, and how to cope."

        response = model.generate_content(prompt)
        
        def format_content(text):
            lines = text.splitlines()
            formatted_lines = []
            i = 0
            j = 0
            for line in lines:
                if line.startswith("**"):
                    if (i!=0) and (j!=0):
                        formatted_lines.append(f"<hr>")
                        formatted_lines.append(f"<h5>{line[2:-2]}</h5>")
                        
                    else:
                        formatted_lines.append(f"<h5>{line[2:-2]}</h5>")
                        i = i + 1
                    
                elif line.startswith("*"):
                    if line[2] == "*":
                        parts = line.split(":")
                        parts[0] = find_all_and_replace(parts[0], "* **")
                        parts[1] = find_all_and_replace(parts[1], "**")
                        formatted_lines.append(f"<strong>{parts[0]}: </strong>{parts[1]}")
                        j = j + 1
                    else:
                        formatted_lines.append(f"- {line[1:]}") 
                        j = j + 1
                else:
                    formatted_lines.append(line)
            return "<br>".join(formatted_lines) 

        formatted_content = format_content(response.text)
        print(videos.get(prediction[0], []))

        context = {
            "issue": current_issue["issue"],
            "description": current_issue["description"],
            "generated_content": formatted_content,
            "videos": videos.get(prediction[0], []),
        }

        return render(request, 'baseApp/result.html', context)
    
    else:
        # If the request method is GET, just render the form
        return render(request, 'baseApp/test.html')
        
    
