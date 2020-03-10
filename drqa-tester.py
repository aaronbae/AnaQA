import drqa.reader
drqa.reader.set_default('model', './data/reader/single.mdl')
reader = drqa.reader.Predictor()  # Default model loaded for prediction


d = "The Super Bowl is the annual championship game of the National Football League (NFL) played between mid-January and early February. It is the culmination of a regular season that begins in the late summer of the previous year."
q = "What is the name of the championship game of the National Football League?"

reader.predict(d, q, candidates=None, top_n=1)
