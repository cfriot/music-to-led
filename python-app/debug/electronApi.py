import numpy as np
import zerorpc
import json, time

# import socketio
# create a Socket.IO server
# sio = socketio.Server()

class ElectronApi():

    def __init__(self, shared_list):
        self.shared_list = shared_list
        self.strip = shared_list[0].strips[0]

    def getInfos(self, text):

        # print("config from api", self.shared_list[0])
        # print(self.shared_list[0].strips[0].is_mirror)

        config_json = self.shared_list[0].getJsonFromSettings()

        audios = []

        for i in range(len(self.shared_list[1])):
            audios.append(self.shared_list[1][i].tolist())

        audios_json = json.dumps(audios)

        strips = []
        # print("toto", len(self.shared_list))
        for i in range(len(self.shared_list) - 2):
            new_strip = self.shared_list[2 + i]
            strips.append(new_strip.tolist())
            # strips.append(self.shared_list[2 + i])

        strips_json = json.dumps(strips)

        infos = "{ \"config\":" + config_json + ", \"audios\":" + audios_json + ", \"strips\":" + strips_json + "}"

        return infos

def apiProcess(shared_list):


    addr = 'tcp://127.0.0.1:8000'
    api = ElectronApi(shared_list)
    s = zerorpc.Server(api)
    s.bind(addr)
    print('* Init Api process --> running on {}'.format(addr))
    s.run()


if __name__ == '__main__':

    from settings.settingsLoader import SettingsLoader

    settingsLoader = SettingsLoader("settings/settings_file.yml")
    config = settingsLoader.data

    apiProcess([config])
