''' Module for the MemeSimCommand class. '''

class MemeSimCommand(object):

    ''' MemeSimCommand represents a command to be sent to the simulator '''

    CommandList = ['rq', 'mq', 'ip', 'pi', 'tm', 'pc', 'lc', 'ca', 'db', 'rs']

    def __init__(self, cmdtype, cmdargs):
        if not cmdtype in MemeSimCommand.CommandList:
            raise Exception('Not a valid command type.')
        self._cmdtype = cmdtype
        self._cmdargs = cmdargs

    def asstring(self):
        ''' Return a string for the command to be sent on the TCP connection to the simulator. '''
        # turn all arguments into strings
        strargs = [str(a) for a in self._cmdargs]
        # return the result
        return self._cmdtype+'!'+ '!'.join(strargs)
        
    @staticmethod
    def RQ(team_id, robot_id):
        return MemeSimCommand('rq', [team_id, robot_id])
    
    @staticmethod
    def MQ(team_id, robot_id, number):
        return MemeSimCommand('mq', [team_id, robot_id, number])
    
    @staticmethod
    def IP(team_id, robot_id, iID):
        return MemeSimCommand('ip', [team_id, robot_id, iID])
    
    @staticmethod
    def PI(team_id, robot_id, iID):
        return MemeSimCommand('pi', [team_id, robot_id, iID])
    
    @staticmethod
    def TM(team_id, robot_id, genome, iID):
        return MemeSimCommand('tm', [team_id, robot_id, genome, iID])
    
    @staticmethod
    def PC(team_id, robot_id, name,genome):
        return MemeSimCommand('pc', [team_id, robot_id, name,genome])

    @staticmethod
    def LC(team_id, robot_id, name,budget):
        return MemeSimCommand('lc', [team_id, robot_id, name,budget])
    
    @staticmethod
    def CA(team_id):
        return MemeSimCommand('ca', [team_id])
    
    @staticmethod
    def DB(team_id):
        return MemeSimCommand('db', [team_id])

    @staticmethod
    def RS(team_id, robot_id, x_pos, y_pos, angle):
        return MemeSimCommand('rs', [team_id, robot_id, x_pos, y_pos, angle])
