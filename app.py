from pickle import TRUE
from flask import request
from flask import Flask, render_template, redirect, url_for
import csv, os
import math
import pandas as pd
import time
import requests

app = Flask(__name__)

#changing url to "home" instead of "/index.html"
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

#changing url to "assessment" instead of "/userdetails.html"
@app.route("/assessment", methods =["GET", "POST"])
def assessment():
    return render_template("userdetails.html")

#retry function in case error unknown occurs, function runs again
def retry(func, retries=3):
    def retry_wrapper(*args, **kwargs):
        attempts = 0
        while attempts < retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                time.sleep(2)
                attempts += 1

    return retry_wrapper

#results page
@app.route("/results", methods =["GET", "POST"])
@retry
def results():
    #getting user details from form
    data = request.form;
    #if user details are missing data (which is a dictionary) will be empty and results page will redirect user to home
    if bool(data) == False:
        return render_template('index.html');
    #getting user details from data
    fname = data['fname'];
    gender = data['gender'];
    country = data['country'];
    email = data['femail'];
    age = data['age'];
    lifeStage = data['life'];
    #getting keys from data dictionary so results can be extracted
    dataKeys = data.keys();
    questions = [];

    for x in dataKeys:
        if "cat" in x:
            questions.append(x);
        else:
            continue
    categories = [];
    for q in questions:
        new = q.split("c");
        if new in categories:
            continue
        else:
            categories.append(new);
    sections = [];
    l = [];
    for c in categories:
        li = [];
        for e in questions:
            if c[1] in e and e not in l:
                li.append(e);
                l.append(e);
            else:
                continue
        if len(li) > 0:
            sections.append(li);
    i = 0;
    scores = [];
    while i < len(sections):
        sco = [];
        for sec in sections[i]:
            y = data[sec];
            sco.append(y);
        total = 0;
        for d in sco:
            total += int(d)
        scores.append(math.ceil((total/48)*100));
        i += 1;

    emailresult = open("/static/data/ResultData.csv");
    csvreads = csv.reader(emailresult);
    resultheader = next(csvreads);
    resultIndex = resultheader.index(" Email");
    rowdatas = [];
    for row in csvreads:
        rowdatas.append(row[resultIndex]);
    emailresult.close()

    DataToCSV = [];
    DataToCSV.append(fname);
    DataToCSV.append(gender);
    DataToCSV.append(country);
    DataToCSV.append(email);
    DataToCSV.append(age);
    DataToCSV.append(lifeStage);
    for s in scores:
        DataToCSV.append(s);
    rq=0;
    for i in scores:
        rq=rq+i;
    rq = rq/5;
    DataToCSV.append(rq);
    if email in rowdatas:
        emailIndex = rowdatas.index(email);
        df = pd.read_csv("/static/data/ResultData.csv")
        p = 0;
        for x in resultheader:
            df.loc[emailIndex, x] = DataToCSV[p];
            p += 1;
        df.to_csv("/static/data/ResultData.csv", index=False);
        
    else:
        f = open('/static/data/ResultData.csv', 'a', newline='')
        writer = csv.writer(f) 
        writer.writerow(DataToCSV)
        f.close()   


    pillars = ["Self-belief", "Purpose", "Adaptability", "Resourcefulness", "Kindred Spirits"];
    dictio = {};
    i = 0;
    while i < len(scores):
        if scores[i] in dictio:
            dictio[scores[i]].append(pillars[i]);
            i += 1;
        else:
            dictio[scores[i]] = [pillars[i]];
            i += 1;
    dico = {};
    num = 0;
    for i in pillars:
        dico[i] = scores[num];
        num += 1;
    
    Max = max(scores);
    Min = min(scores);
    strength = [];
    for x in dictio[Max]:
        strength.append([x])
    weakness = [];
    for s in dictio[Min]:
        if dictio[Min] == dictio[Max]:
            continue
        else: 
            weakness.append([s])
    NeutralScores = [];
    for i in scores:
        if i == Max or i == Min:
            continue
        else:
            NeutralScores.append(i)
    NeutralScores.sort();
    neutral = [];
    for i in NeutralScores:
        for f in dictio[i]:
            neutral.append([f])
    neutrall = [];
    for n in neutral:
        if n in neutrall:
            continue
        else:
            neutrall.append(n);

    title = ["Adaptability", "Kindred Spirits", "Purpose", "Resourcefulness", "Self-belief"];
    titletext = ["Able and willing to adjust your actions and approach to adapt to a different environment. To be future-oriented in overcoming and anticipating tasks, transitions, and setbacks. To stay relevant by embracing change with an open mind and a learner’s attitude.",
    "To build strong networks and have open and trusting relationships. Willing to be vulnerable and seek help from a group of trusted people (e.g. friends, family, mentors) that act as a pillar of support in your career journey.",
    "To have a sense of direction in your life and career, equipped with a clear vision, and to act with intention and determination to achieve it. Connected to a sense of meaning, fulfilment, and satisfaction in your work.",
    "Know how to achieve your goals by tapping on relevant resources and networks skillfully. Know when and where to seek help. Make bold moves to achieve a desired outcome. Able to maximise opportunities and connect the dots.",
    "Confidence in your capabilities, judgement and ability to overcome challenges or accomplish a goal. To have positive feelings about yourself and have the courage to act on your beliefs. Includes having a growth mindset too."]
    results = []; #get results from CVS file
    
    Stratstitle = ["Strategies to develop Adaptability",
    "Strategies to grow your Kindred Spirits",
    "Strategies to develop Purpose",
    "Strategies to develop Resourcefulness",
    "Strategies to build Self-belief"]
    Strats = ["The Kubler Ross Change Curve describes three stages of coping with change: shock and denial, anger and depression, and finally acceptance. Everyone facing change goes through the same emotional cycle, but not at the same pace. How can you move through the cycle faster? To adapt well, you have to see the need to adapt, determine the right methods of adaptation and integrate them into your actions and attitude. Adaptability requires thinking more astutely, creatively and openly.",
    "Knowing the important people in your life and the dynamics of the relationships you have with them is a great starting point in forming your own group of kindred spirits. The connections and chemistry you have with them are typically mutual, where you feel comfortable confiding in them, and vice versa. Here are some ways you can go about acknowledging and developing relationships with those around you:",
    "“Purpose” is a big word - you’d first have to develop a strong sense of your own individual purpose, distil your purpose into a concrete statement, and then turn it into action.",
    "To be resourceful means being able to create useful and unique solutions in challenging situations, with what you have.",
    "What self-limiting beliefs do you hold that stop you from progressing forward? If you wish to boost your self-belief, here are some practical ways to do so powerfully:",];
    
    strat1header = ["Keep your eyes on the overarching goal - what does it mean to “win”?",
    "Map your inner circle",
    "Strategies to develop Purpose",
    "Get curious",
    "Understand your strengths and learn how to maximise them"]
    strat1text = ["Look beyond coping and surviving by limiting your losses, and incorporating them into your overall strategy of achieving your long-term purpose.",
     "Make a list of people in your life that you can trust and rely on when seeking support and advice throughout your career journey. They may include your loved ones, co-workers, friends, and mentors; preferably a diverse range of people who can help you in different areas of your life.",
     "“Purpose” is a big word - you’d first have to develop a strong sense of your own individual purpose, distil your purpose into a concrete statement, and then turn it into action.",
     "Nurture your curiosity and willingness to explore new options. Learn not only when you are necessitated to, but all the time, about different subjects and topics. This helps you to form connect the dots and ideate innovative solutions that others may find difficult to form in the same situation.",
     "Ask 3 friends and family what they think you are naturally good at. If you find yourself saying “it doesn’t feel like a strength”, remind yourself of this proverb: Fish finds water last. What is naturally easy for you may not be easy for others at all! Take pride in your strengths and learn how you can apply them in your career. If you find yourself absolutely unable to use your strengths in your current job, ask yourself if you’d be happier in another industry/job function."]
    
    strat2header = ["Build the ability to Unlearn",
    "Confront your fears",
    "Invite others to review your Purpose together to help you go deeper",
    "Start by redefining what’s possible and be willing to take risks",
    "Build a growth mindset and develop a strong internal locus of control"]
    strat2text = ["Look beyond coping and surviving by limiting your losses, and incorporating them into your overall strategy of achieving your long-term purpose.",
    "What are some of the issues you currently face that you have been procrastinating to address? Make a plan to hold an open and honest conversation with the relevant people you have identified above to talk through your issues.",
    "Your Kindred Spirits can act as a powerful sounding board and a listening ear, but the memories and ideas have to come from you alone.",
    "Be open-minded and don’t undermine your capabilities before you actually put them to use. You may not be sure how others will view your actions and decisions when you take an unconventional approach, but it pays off when you are able to solve problems others cannot.",
    "Growth mindset is the belief that our basic abilities can be improved through hard work and effort. Remind yourself that failure just gives you an opportunity to improve in future; they are not the end of the road. Building a strong internal locus of control means knowing that the events in your life are primarily the result of your actions. You have a lot of power to change the course of your future."]
    
    strat3header = ["Be good at learning how to do new things and experiment",
    "Build positive, healthy relationships",
    "Craft your Purpose statement",
    "Break some rules",
    "Practice self-compassion and affirmation"]
    strat3text = ["Gone are the times when you only have to be really good at a few key aspects important to your role. As we move into the Future of Work, roles and skills are becoming increasingly blurred. To accomplish ever-changing goals, companies are moving away from fixed job scopes and embracing employees who are willing to put their hand up to contribute new expertise outside of their ordinary “scope” of work.",
    "Which relationships would you like to further strengthen? E.g. a few particular people you felt you have neglected or stopped interacting with for a while now.",
    "A Purpose statement succinctly summarises what makes life meaningful to you and how you would like to live your life. You will know that you have defined your statement well when you feel a deep conviction and feel emotionally engaged. The best purpose statements also call you strongly to take action.",
    "You cannot be resourceful and creative without thinking outside the box. And to do so, you may need to deviate from the established “norms”. Of course, this starts with knowing what type of rules you can break (nothing immoral or unethical). If you find a rule too rigid, of lower importance and isn’t against the law, and know that going around it may give you an operational advantage, consider solving the problems from different angles even if you may step on a few toes unintentionally along the way.",
    "We are often the harshest critic of ourselves. Imagine yourself talking to your best friend: What will you say to him/her when they are hurting, or when they face a setback? Use the same gentle language and tone of voice with yourself."]
    
    strat4header = ["Learn to take baby steps into the unknown",
    "Reshape your relationship dynamics",
    "Craft your development plan",
    "Don’t just be reactive to external circumstances",
    "Accomplish something small every day"]
    strat4text = ["Embrace the fact that you might fail in some strategies and plans, and you may even take detours that end up not yielding any fruit at the end of the day. Keep a positive attitude along the way and have faith that these ups and downs may one day be your source of inspiration to help you achieve your dream.",
    "What areas would you like to improve in terms of how you interact and communicate with your potential group of kindred spirits? (and make an intention to work on them) - E.g. being less judgemental, active listening, showing empathy, and offering constructive comments and advice.",
    "It is not enough to have a Purpose statement without a clear action plan. Break down your development plan to lean into your purpose, into three to five-year goals, two-year goals, and lastly, one-year goals. Think of the critical next steps you must take in the coming few months. ",
    "Be more proactive in engaging and influencing the situation and people around you to create the change you want to see. It’s always desirable to foresee a future challenge and already build towards managing it before it comes.",
    "Even something as small as exercising for 5 minutes, or making your bed, boosts your self-perception. There is nothing more important than being able to trust yourself and your ability to get things done. Setting goals and accomplishing them successfully teach your brain to have faith in you, and gives it confidence that you can be relied on to solve future problems."]
    
    strat5header = ["Adopt an adventurous mindset and take a leap of faith",
    "Give (more) and take",
    "Consider the key relationships you need to manifest your purpose",
    "Leverage your existing resources",
    "Pursue an external hobby"]
    strat5text = ["Sometimes change can be exciting, especially if you get to experience something new that has never been done before. Try to focus on the positive and beneficial aspects of this new environment or role that you are involved in instead of just fixating on the negative aspects.",
    "Most importantly, think about what and how you can give in the relationships that matter to you (as much as you get, if not more).",
    "Who are the people in your life that have a similar goal, or who are supportive of your goals? If you find that the bulk of your dream lies outside of the support your social circle can provide you, look out for opportunities to join communities that you resonate with. Seek out mentors within or outside your company.",
    "First, start off by knowing the resources at your command. How many people are there working in your team, and what are their strengths and skills? What information or technology do you wield that may be useful? Leveraging the professional network of you and your team - peer groups, groups above you, or leaders in other organisations - may also help you solve existing problems.",
    "If you’re feeling helpless in your career, try to find mastery in another area of your life. It will help you to build self-efficacy (one's belief in one's ability to succeed in specific situations or accomplish a task), and this, in turn, builds up your self-esteem, which transcends to other areas of your life including your career."]

    
    file = open('/static/data/ResultData.csv')
    csvreader = csv.reader(file)
    rows = [];
    for row in csvreader:
        rows.append(row);
    header = rows[0];
    KsIndex = header.index(" Kindred Spirits");
    SbIndex = header.index(" Self Belief");
    PIndex = header.index(" Purpose");
    RIndex = header.index(" Resourcefulness");
    AIndex = header.index(" Adaptability");
    RQIndex = header.index(" RQ")
    i = 1;

    KsMedian = 0;
    SbMedian = 0;
    PMedian = 0;
    RMedian = 0;
    AMedian = 0;
    RQMedian = 0;
    while i < len(rows):
        KsMedian += float(rows[i][KsIndex]);
        SbMedian += float(rows[i][SbIndex]);
        PMedian += float(rows[i][PIndex]);
        RMedian += float(rows[i][RIndex]);
        AMedian += float(rows[i][AIndex]);
        RQMedian += float(rows[i][RQIndex]);
        i += 1;
    KsMedian = round(KsMedian/(i-1));
    SbMedian = round(SbMedian/(i-1));
    PMedian = round(PMedian/(i-1));
    RMedian = round(RMedian/(i-1));
    AMedian = round(AMedian/(i-1));
    RQMedian = round(RQMedian/(i-1));
    file.close();
    resultsx = open("/static/data/Results.csv");
    csvread = csv.reader(resultsx);
    dico["resilient quotient"] = rq;
    rowdata = [];
    for row in csvread:
        rowdata.append(row);
    start = 2;
    pillars.append("resilient quotient");
    textresult = [];
    while start < len(rowdata):
        if rowdata[start][0] in pillars:
            score = dico[rowdata[start][0]];
            index = 1;
            while score <= int(rowdata[0][index]):
                index += 1;
            textresult.append([rowdata[start][0], rowdata[start][index]]);
            start += 1;
        else:
            start += 1;
    b = 0;
    rn = 0;
    while b < len(title):
        if textresult[rn][0] == title[b]:
            results.append(textresult[rn][1]);
            rn = 0;
            b += 1;
        else:
            rn += 1;
    resultsx.close()
    imagenumbering = [1,2,3,4,5];
    #1: "Adaptability", 2: "Kindred Spirits", 3: "Purpose", 4: "Resourcefulness", 5: "Self-belief"
    
    #adding strenghts info into list so it can be sent to the frontend
    for i in strength:
        z = 0;
        while z < len(title):
            if title[z] == i[0]:
                i.append(titletext[z]);
                i.append(Stratstitle[z]);
                i.append(Strats[z]);
                i.append(strat1header[z]);
                i.append(strat1text[z]);
                i.append(strat2header[z]);
                i.append(strat2text[z]);
                i.append(strat3header[z]);
                i.append(strat3text[z]);
                i.append(strat4header[z]);
                i.append(strat4text[z]);
                i.append(strat5header[z]);
                i.append(strat5text[z]);
                i.append(imagenumbering[z]);
                i.append(results[z]);
                z += 1;
            else:
                z += 1;
    #adding weaknesses info into list so it can be sent to the frontend
    for i in weakness:
        z = 0;
        while z < len(title):
            if title[z] == i[0]:
                i.append(titletext[z]);
                i.append(Stratstitle[z]);
                i.append(Strats[z]);
                i.append(strat1header[z]);
                i.append(strat1text[z]);
                i.append(strat2header[z]);
                i.append(strat2text[z]);
                i.append(strat3header[z]);
                i.append(strat3text[z]);
                i.append(strat4header[z]);
                i.append(strat4text[z]);
                i.append(strat5header[z]);
                i.append(strat5text[z]);
                i.append(imagenumbering[z]);
                i.append(results[z]);
                z += 1;
            else:
                z += 1;
    neutral.sort(); #sorting results from lowest to highest

    #adding neutral info into list so it can be sent to the frontend
    for i in neutrall:
        z = 0;
        while z < len(title):
            if title[z] == i[0]:
                i.append(titletext[z]);
                i.append(Stratstitle[z]);
                i.append(Strats[z]);
                i.append(strat1header[z]);
                i.append(strat1text[z]);
                i.append(strat2header[z]);
                i.append(strat2text[z]);
                i.append(strat3header[z]);
                i.append(strat3text[z]);
                i.append(strat4header[z]);
                i.append(strat4text[z]);
                i.append(strat5header[z]);
                i.append(strat5text[z]);
                i.append(imagenumbering[z]);
                i.append(results[z]);
                z += 1;
            else:
                z += 1;
    #change text based on rq if it is higher or lower than rq median
    if rq > RQMedian:
        highorlow = "higher than"
    else:
        highorlow = "lower than"

    #sending results to the frontend
    return render_template("results.html", sb = scores[0], p = scores[1], a = scores[2], r = scores[3], ks = scores[4], name = fname, strength = strength, weakness = weakness, neutral= neutrall, rq=rq, AMedian = AMedian, KsMedian = KsMedian, PMedian=PMedian, RMedian = RMedian, SbMedian=SbMedian, RQMedian = RQMedian, highorlow = highorlow )

if __name__=='__main__':
   app.debug = True
   app.run(host="0.0.0.0")

