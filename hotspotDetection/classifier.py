from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import argparse
import pickle
import h5py

ap = argparse.ArgumentParser()
ap.add_argument("-train",  "--train_hdf5", required=True, help="path to trained hdf5 file")
ap.add_argument("-test", "--test_hdf5", required=True, help="path to test hdf5 file")
args = vars(ap.parse_args())


db_training = h5py.File(args["train_hdf5"], "r")
db_testing = h5py.File(args["test_hdf5"], "r")

print ("[INFO] tuning hyperparameters")

params = {"C": [0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]}
model = GridSearchCV(LogisticRegression(), params, cv=3,n_jobs=-1)

#model = LogisticRegression(C=0.1, n_jobs=-1)

model.fit(db_training["features"][:], db_training["labels"][:])


print("[INFO] best hyperparameters: {}".format(model.best_params_))
#evaluate model...

preds = model.predict(db_testing["features"][:])
print (classification_report(db_testing["labels"][:], preds, target_names=db_testing["label_names"][:]))

#save to disk..

f = open("model.cpickle", "wb")
f.write(pickle.dumps(model.best_estimator_))
f.close()
#close database
db_training.close()
db_testing.close()
