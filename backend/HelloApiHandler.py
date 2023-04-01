from flask_restful import Api, Resource, reqparse
import cohere

# cohere


class HelloApiHandler(Resource):
  
  def get(self):

    prompt = f"""
      this program gives age, name, occupation, aspiratoin, and summary based on a paragraph 

      Paragraph: Hi my name is kevin and I am 19 years old. i currently work at caribou contests where i develop websites. I am currently a CS/BBA student and I hope to work for Google someday. 
      Age: 19
      Name: Kevin
      Occupation: Web Developer
      Aspiration: Kevin hopes to work for Google someday
      Summary: Kevin, a 19 year old CS/BBA student is currently a Web Developer for Caribou Contests. He hopes to work for Google someday. 
      --
      Paragraph: my name is andy, a 80 year old and i currently work for orbiseed developing react applications. I am a current CS student with aspirations to work for big tech as a software developer in the near future. My interests include participating in hackathons and gaming. 
      Age: 80
      Name: Andy
      Occupation: React Developer
      Aspiration: Andy aims to be a software developer for a big tech company
      Summary: Andy is an 80 year old current React Developer for Orbiseed. He currently studies CS and aspires to work for big tech as a software developer. His interests include participating in hackathons and gaming. 
      --
      Paragraph: im bob and im currently unemployeed. im 37 years old and have an apprenticeship for an electrician. i hope to find a job in construction some day. i love building and constructing various things using my hands and am very skilled in this field. 
      Age: 9
      Name: Bob
      Occupation: unemployeed
      Aspiration: Bob hopes to work in construction
      Summary: Bob is a 37 year old who has completed an electrician apprenticeship. Although currenlty being unempolyeed, he hopes to find work in the construction field. Bob loves building and constructing various things using his hands and is very skilled in this field. 

      --

      Paragraph: Good morning I am sam, a 20 year old student living in windsor. I currently work as an intern for the government. I love journally and writing articles on Medium. I hope to continue my path and work for the governemnt when i graduate.
      Age: 20
      Name: Sam
      Occupation: Government Intern
      Aspiration: Sam hopes to work for the government when he graduates
      Summary: Sam is a 20 year old student working as a Government Intern. He loves journally and writing articles on Medium. He hopes to continue his path and work for the governemnt when he graduates. 

      --

      Paragraph: Hello, I'm josh. I'm an IT tech for a local company. I'm 23 years old. I live in oakland. I love watching football and playing with my dog. 
      Age: 23
      Name: Josh
      Occupation: IT Tech
      Aspiration: Josh is an IT tech for a local company
      Summary: Josh is a 23 year old IT tech for a local company. He lives in Oakland. He loves watching football and playing with his dog.

      --

      Paragraph: Hey, I'm Joey. I'm a student who is currently 23 years old. One day I hope to be an amazing farmer just like my dad and take over the family ranch.
    """

    co = cohere.Client('BMA8m2BTfZL8evBDjd05ctLFlgKtkARvn7jJbYgq')

    response = co.generate(
      model='command-xlarge-nightly',  
      prompt = prompt,  
      max_tokens=100,
      num_generations = 1,  
      temperature=0.6,  
    )

    res = response.generations[0].text

    ageIndex = res.index("Age:")
    nameIndex = res.index("Name:")
    occupationIndex = res.index("Occupation:")
    aspirationIndex = res.index("Aspiration:")
    summaryIndex = res.index("Summary:")

    ageString = res[ageIndex + 5 : nameIndex]
    nameString = res[nameIndex + 6 : occupationIndex]
    occupationString = res[occupationIndex + 12 : aspirationIndex]
    aspirationString = res[aspirationIndex + 12 : summaryIndex]
    summaryString = res[summaryIndex + 9 : ]

    return {
      'resultStatus': 'SUCCESS',
      'age': '{}'.format(ageString),
      'name': '{}'.format(nameString),
      'occupation': '{}'.format(occupationString),
      'aspiration': '{}'.format(aspirationString),
      'summary': '{}'.format(summaryString)
      }

  def post(self):
    print(self)
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str)
    parser.add_argument('message', type=str)

    args = parser.parse_args()

    print(args)
    # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')

    request_type = args['type']
    request_json = args['message']
    # ret_status, ret_msg = ReturnData(request_type, request_json)
    # currently just returning the req straight
    ret_status = request_type
    ret_msg = request_json

    if ret_msg:
      message = "Your Message Requested: {}".format(ret_msg)
    else:
      message = "No Msg"
    
    final_ret = {"status": "Success", "message": message}

    return final_ret
