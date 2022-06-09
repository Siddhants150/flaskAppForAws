from flask import Flask, render_template, url_for, request
import boto3
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == "POST":
        try:
            req = request.form['content']
            session = boto3.Session(profile_name = 'siddhantIntern')
            s3 = session.client("s3")
            bucketName = "tiger-mle-pg"
            response = s3.list_objects_v2(Bucket = bucketName, Prefix = "home/siddhant.sharma/", Delimiter = "/")
            subFolders = []
            for i in response.get("CommonPrefixes"):
                subFolders.append(i.get("Prefix"))
            s3Resource = session.resource("s3")
            bucket = s3Resource.Bucket(bucketName)
            dic = {}
            for i in subFolders:
                for j in bucket.objects.filter(Prefix = i):
                    if j.key!=i:
                        if i not in dic.keys():
                            dic[i] = [j.key.replace(i, "")]
                        else:
                            dic[i].append(j.key.replace(i, ""))
            displayName = "home/siddhant.sharma/" + req.upper() + "/"
            # req.upper()
            return render_template("index.html", dic = dic[displayName])
        except Exception as e:
            print(e)
        return "Hello World"
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = False)