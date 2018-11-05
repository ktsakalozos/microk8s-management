from subprocess import check_output

from flask import Flask
from flask_restful import reqparse, Resource, Api

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('status')


class Ping(Resource):
    def get(self):
        return {'ping': 'pong'}


class AddonsList(Resource):
    def get(self):
        cmd = "microk8s.enable --help".split()
        output = check_output(cmd)
        addons = []
        addons_started = False
        for line in output.split('\n'):
            line = line.strip()
            if len(line) <= 0:
                continue
            print(line.strip())

            if line == "Available addons:":
                addons_started = True
                continue
            if addons_started:
                addons.append(line)

        return addons


class Addon(Resource):

    def put(self, addon):
        args = parser.parse_args()
        status = args['status'].decode("utf8")
        print("Changing {} to {}".format(addon, status))
        cmd = "microk8s.{} {}".format(status, addon).split()
        check_output(cmd)
        return "ok"


api.add_resource(Ping, '/')
api.add_resource(AddonsList, '/v1/addons')
api.add_resource(Addon, '/v1/addons/<addon>')


if __name__ == '__main__':
    app.run(debug=True)