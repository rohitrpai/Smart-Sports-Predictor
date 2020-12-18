import pandas as pd
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder


def predictor(team1, team2):
    matches=pd.read_csv('matches.csv')
    df = matches[['date', 'team1', 'team2', 'result', 'winner', 'venue']].copy()
    totalwins1=0
    totalwins2=0
    count1 = 0
    count2 = 0
    result = ''
    pred = ''
    date=''
    df_2 = df.loc[(df['team1'] == team1) & (df['team2'] == team2)]
    df_3 = df.loc[(df['team1'] == team2) & (df['team2'] == team1)]
    df_final = pd.concat([df_2, df_3])
    df_final.reset_index(drop=True, inplace=True)
    df_final = df_final.drop('result', axis=1)
    df_final = df_final.drop('date', axis=1)
    df_final = df_final.drop('venue', axis=1)
    df_final.loc[df_final['team1'] == team1, 'team1'] = 1
    df_final.loc[df_final['team1'] == team2, 'team1'] = 2
    df_final.loc[df_final['team2'] == team1, 'team2'] = 1
    df_final.loc[df_final['team2'] == team2, 'team2'] = 2
    df_final.loc[df_final['winner'] == team1, 'winner'] = 1
    df_final.loc[df_final['winner'] == team2, 'winner'] = 2

    X_train = df_final.drop('winner', axis=1)
    y_train = df_final['winner']

    if(X_train.empty or y_train.empty):
        y_pred="\nThese teams have never faced each other until now! \n\n Overall: \n"+team1+" wins: "+str(totalwins1)+", "+team2+" wins: "+str(totalwins2)+"\n"
    else:
        teams = [[1,2]]
        teams = pd.DataFrame(teams)


        X_test = pd.DataFrame(teams)
        print(X_test)

        model = GaussianNB()
        #X = preprocessing.scale(X)

        #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=101)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        if y_pred == 1:
            y_pred = team1
        else:
            y_pred = team2

    for ind in df.index:
        if((df['team1'][ind]==team1 or df['team2'][ind]==team1) and (df['team1'][ind]==team2 or df['team2'][ind]==team2)):
            result = df['winner'][ind]
            date = df['date'][ind]
            venue = df['venue'][ind]
            if result==team1:
                count1+=1
            else:
                count2+=1

    for ind in df.index:
        if((df['team1'][ind]==team1 or df['team2'][ind]==team1) and (df['winner'][ind]==team1)):
            totalwins1+=1
        elif((df['team1'][ind]==team2 or df['team2'][ind]==team2) and (df['winner'][ind]==team2)):
            totalwins2+=1

    if count1==0 and count2==0:
        pred="\nThese teams have never faced each other until now! \n\n Overall: \n"+team1+" wins: "+str(totalwins1)+", "+team2+" wins: "+str(totalwins2)+"\n"
    elif count1==count2:
        pred="\nIt is too close to call. \n\nHead to Head: \n"+team1+" wins: "+str(count1)+", "+team2+" wins: "+str(count2)+"\n\n Overall: \n"+team1+" wins: "+str(totalwins1)+", "+team2+" wins: "+str(totalwins2)+"\n\n Last time the two teams met was on "+str(date)+" at "+venue+" and "+result+" won."+"\n"
    else:
        pred = "\nAs per our predictions, " + y_pred + " has higher chances of winning. \n\nHead to Head: \n" + team1 + " wins: " + str(
            count1) + ", " + team2 + " wins: " + str(count2) + "\n\n Overall: \n" + team1 + " wins: " + str(
            totalwins1) + ", " + team2 + " wins: " + str(totalwins2) + "\n\n Last time the two teams met was on " + str(
            date) + " at " + venue + " and " + result + " won." + "\n"

    pred = pred.replace('\n', '<br>')
    return pred
