import kenlm

#model = kenlm.Model('srilm-voxforge-de-r20171217.arpa')
model = kenlm.Model('cmusphinx-voxforge-de.lm')

print(model.score("in der hand", bos = False, eos = False)) # Größerer Score = ist wahrscheinlicher!
print(model.score("in der hund", bos = False, eos = False))



# Großgeschriebene Wörter sind out-of-vocabulary!

scores = model.full_scores("Hand", bos=False, eos=False) # returns dtype Class Generator
scores = next(scores) # returns dtype tuple
print(scores)
print("Hand","Probability:", scores[0], ", N-Gram Length:", scores[1], ", OOV:", scores[2])

scores = model.full_scores("hand", bos=False, eos=False)
scores = next(scores)
print("hand", "Probability:", scores[0], ", N-Gram Length:", scores[1], ", OOV:", scores[2])

#Satzzeichen auch!

scores = model.full_scores(".", bos=False, eos=False)
scores = next(scores)
print(".", "Probability:", scores[0], ", N-Gram Length:", scores[1], ", OOV:", scores[2])
    


# aufgedröseltes Beispiel
print('*'*100)
scores = model.full_scores("auf der einen seite", bos=False, eos=False) # scores is dtype class Generator
for score in scores:
    print(score)
    print("auf der einen seite", "Probability: ", score[0], ", N-Gram Length:", score[1], ", OOV:", score[2])
print("auf der einen seite", "Gesamtprobability: ", model.score("auf der einen seite"))

print('*'*100)
scores = model.full_scores("dodo belt den eismann an", bos=False, eos=False)
for score in scores:
    print(score)
    print("dodo belt den eismann an", "Probability: ", score[0], ", N-Gram Length:", score[1], ", OOV:", score[2])
print("dodo belt den eismann an","GESAMTPROBABILITY: ", model.score("in der hand"))

print('*'*100)
scores = model.full_scores("Dodo belt den Eismann an", bos=False, eos=False)
for score in scores:
    print(score)
    print("Dodo belt den Eismann an", "Probability: ", score[0], ", N-Gram Length:", score[1], ", OOV:", score[2])
print("Dodo belt den Eismann an","GESAMTPROBABILITY: ", model.score("in der hund"))

t1 = "der eismann rückt dodo an"
t2 = "der eismann zückt dodo an"
t3 = "der eismann guckt dodo an"

tX = ". dodo belt den eismann"
tX2 = "dodo belt den eismann"
tX3 = "kaufen dodo belt den eismann"

print('-'*100)

scores = model.full_scores(t1, bos=False, eos=False)
for score in scores:
    print(score)
    print("Probability: ", score[0], ", N-Gram Length:", score[1], ", OOV:", score[2])
print("GESAMTPROBABILITY: ", model.score(t1))

scores = model.full_scores(t2, bos=False, eos=False)
for score in scores:
    print(score)
    print("Probability: ", score[0], ", N-Gram Length:", score[1], ", OOV:", score[2])
print("GESAMTPROBABILITY: ", model.score(t2))

scores = model.full_scores(t3, bos=False, eos=False)
for score in scores:
    print(score)
    print("Probability: ", score[0], ", N-Gram Length:", score[1], ", OOV:", score[2])
print("GESAMTPROBABILITY: ", model.score(t3))

scores = model.full_scores(tX, bos=False, eos=False)
for score in scores:
    print(score)
    print("Probability: ", score[0], ", N-Gram Length:", score[1], ", OOV:", score[2])
print("GESAMTPROBABILITY: ", model.score(tX))

scores = model.full_scores(tX2, bos=False, eos=False)
for score in scores:
    print(score)
    print("Probability: ", score[0], ", N-Gram Length:", score[1], ", OOV:", score[2])
print("GESAMTPROBABILITY: ", model.score(tX2))

scores = model.full_scores(tX3, bos=False, eos=False)
for score in scores:
    print(score)
    print("Probability: ", score[0], ", N-Gram Length:", score[1], ", OOV:", score[2])
print("GESAMTPROBABILITY: ", model.score(tX3))