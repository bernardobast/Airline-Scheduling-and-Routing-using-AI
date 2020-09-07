### Template ###

import search
import sys

class ASARProblem(search.Problem):

    def __init__(self):
        self.initial = 0# place here the initial state (or 'None')
        #Creates a dictionary of airports
        self.airports = {}
        #Creates a dictionary of planes
        self.planes = []
        #Creates a dictionary with all the legs
        self.legs = Legs()
        #Creates a dictiona for rotation time
        self.rot_time = {}


    def actions(self, state):
        #Action vector to be returned
        actions = []
        #Index that identifies a plane
        plane_id = 0
        #Models
        models = []
        #Flights performed before
        legs_id = []
        #Time of each plane
        time = {}

        for departure_airport in state[0]:
            #Plane model
            model = self.planes[plane_id][1]
            #The plane has not yet been located anywhere
            if departure_airport == 'None':
                #Prevents actions of the same model to be repeated
                if model not in models:
                    actions += self.legs.return_leg_by_model(model)
                    models+=[model]
                else:
                    plane_id += 1
                    continue
            #The plane has been placed
            else:
                actions += self.legs.return_leg_by_name((departure_airport+model))
            #Updates plane id
            plane_id += 1

        #Converts legs done to list
        for sub_list in state[2]:
            legs_id += list(sub_list)

        #Corrected actions vetor
        actions_correct = []

        #Creates a dictionary with key Airport + Model =  time
        for i in range(len(state[0])):
            current_airport = state[0][i]
            #if the current airport is 'None', then the element is not added
            if current_airport != 'None':
                model = self.planes[i][1]
                time[current_airport+model]=state[1][i]


        for i in range(len(actions)):
            #Checks if the action was already performed
            if (actions[i][-1] in legs_id):
                continue
            if actions[i][0]+actions[i][3] in time.keys():
                #Calculates the travelling plus the rotation time
                travel_time = time[actions[i][0]+actions[i][3]]+actions[i][2]+self.rot_time[actions[i][3]]
                #If traveling time is bigger than the closing time of the airport
                if travel_time > self.airports[actions[i][1]][1]:
                    #print('Out Of Time!!!, ', travel_time)
                    continue
            else:
                travel_time = self.airports[actions[i][0]][0]+actions[i][2]
                if travel_time < self.airports[actions[i][1]][0]:
                    continue

            actions_correct += [actions[i]]

        return actions_correct


    def result(self, state, action):
        #Converts the state to a list
        new_state = state_to_list(state)
        #Model of the plane to travel
        model = action[3]
        #Departure and Arrival airport
        departure_airport = action[0]
        arrival_airport = action[1]
        #Time to travel
        time = action[2]
        #Id to store
        id = action[-1]

        #Seach for plane
        for i in range(len(state[0])):
            #Searches for a plane of that model that is in the departure airport
            if(departure_airport==new_state[0][i] and model==self.planes[i][1]):
                new_state[0][i] = arrival_airport
                new_state[2][i] += [id]
                new_state[1][i] +=  time + self.rot_time[model]
                new_state[3] += 1
                return state_to_tuple(new_state)
        #If not found the plane has not been placed yet
        for i in range(len(state[0])):
            #Searches for a ''None'' departure airport and for a plane of that model
            if(new_state[0][i]=='None' and model==self.planes[i][1]):
                new_state[0][i] = arrival_airport
                new_state[2][i] += [id]
                new_state[3] += 1
                #Ads the time the airport opens, the flight time and the rotation time
                new_state[1][i] += self.airports[departure_airport][0]+time + self.rot_time[model]
                return state_to_tuple(new_state)


    def goal_test(self, state):
        #Saves the departure airports
        departure_airports = []

        #Converts legs done to list
        for sub_list in state[2]:
            #Checks if this list is empty
            if len(sub_list)>0:
                departure_airports += [self.legs.return_leg_by_id(sub_list[0])[0]]
            else:
                departure_airports += ['None']

        #Checks if the number of legs is equal to the already done and the planes are in the first airport
        if(state[3]==self.legs.return_nb_legs() and tuple(departure_airports)==state[0]):
            #print('Goal was reached')
            return True
        #If not then the goal is not reached
        else:
            return False
        pass


    def path_cost(self, c, state1, action, state2):
        #Cost function regarding the profit of each flight
        cost = c + 1/action[-2]
        return cost

    def heuristic(self, node):
        # note: use node.state to access the state
        #List of actions that were already performed on that state
        legs_id = []
        reamining_legs = []

        #Converts legs done to list
        for sub_list in node.state[2]:
            legs_id += list(sub_list)

        #Adds the reamining_legs to a list
        for id in range(self.legs.number_of_legs):
            #If the action is not already performed
            if id not in legs_id:
                reamining_legs += [self.legs.return_legs_max_by_id(id)]
        h=0
        if len(reamining_legs)!=0:
            for max_profit in reamining_legs:
                h += (1/max_profit)
        else:
            h=0

        return h


    def load(self, fh):
        # note: fh is an opened file object
        # note: self.initial may also be initialized here
        info = fh.readlines()
        id = 0
        for i in range(len(info)):

            #Reads the first character
            data_type = info[i][0]
            #String containing all the needed data
            data = info[i]

            #If its an airport
            if data_type == 'A':
                str = data.split()
                self.airports[str[1]]=[minute_converter(str[2]), minute_converter(str[3])]

            #If its a plane
            if data_type == 'P':
                str = data.split()
                self.planes.append([str[1],str[2]])

            #If its a Leg
            if data_type == 'L':
                str = data.split()
                #Add a new fight
                index = 4

                #Adds a leg
                self.legs.add_number_of_legs()

                while(index<len(str)):
                    self.legs.add_Leg(str, index, id)
                    index += 2
                id+=1

            #If data is a rotation time
            if data_type == 'C':
                str = data.split()
                self.rot_time[str[1]] = minute_converter(str[2])

        #Computes the initial state
        self.initial = initial_state(self.planes)
        pass


    def save(self, fh, state):
        profit = 0
        if state != None:
            # state to list
            state_to_list(state)
            # note: fh is an opened file object
            for i in range(len(self.planes)):
                str_ = 'S '
                plane_legs = state[2][i]
                if len(plane_legs)!=0:
                    leg = self.legs.return_leg_by_id(plane_legs[0])
                    departure_airport = leg[0]
                    str_ = str_+self.planes[i][0]+' '+hour_converter(self.airports[departure_airport][0])+' '+departure_airport+' '+leg[1]
                    time = self.airports[departure_airport][0]
                    profit += self.legs.return_profit(plane_legs[0], self.planes[i][1]);
                    for j in range(1,len(plane_legs)):
                        profit += self.legs.return_profit(plane_legs[j], self.planes[i][1]);
                        time = time + minute_converter(leg[2]) + self.rot_time[self.planes[i][1]]
                        leg = self.legs.return_leg_by_id(plane_legs[j])
                        str_ = str_+ ' '+ hour_converter(time) + ' '+ leg[0] + ' ' + leg[1]
                    str_ += '\n'
                    fh.write(str_)
            last_line = 'P '+str(profit)
            fh.write(last_line)
        else:
            fh.write('Infeasible.')


class Legs(object):
    """docstring forLegs."""

    def __init__(self):
        #Identifies the leg by
        self.legs = {}
        self.legs_id = {}
        self.legs_id_max = {}
        self.number_of_legs = 0

    def add_Leg(self, str, index, id):
        key = str[1]+str[index]
        #Key is formed by the (airport_name + plane_class)
        if key not in self.legs.keys():
            self.legs[key] = []
        self.legs[key].append([str[1],str[2], minute_converter(str[3]),str[index],float(str[index+1]), id])
        self.legs_id[id]=str[1:]

        #Max profit of each leg by id
        if id not in self.legs_id_max.keys():
            self.legs_id_max[id] = float(str[index+1])
        elif float(str[index+1])>self.legs_id_max[id]:
            self.legs_id_max[id] = float(str[index+1])

    def add_number_of_legs(self):
        self.number_of_legs+=1

    def return_leg_by_model(self, model):
        #List of lists
        pre_info = [value for key, value in self.legs.items() if model in key]
        info = []
        #Puts all information in a list
        for infos_ in pre_info:
            for i in range(len(infos_)):
                info += [infos_[i]]
        return info

    def return_leg_by_name(self, key):
        info = self.legs[key]
        return info

    def return_leg_by_id(self, id):
        info = self.legs_id[id]
        return info

    def return_profit(self, id, model):
        info = self.legs_id[id]
        profit = info[info.index(model)+1]
        return float(profit)

    def return_legs_max_by_id(self, id):
        info = self.legs_id_max[id]
        return info

    def return_nb_legs(self):
        return self.number_of_legs



#####       Defines the initial state           ######
def initial_state(planes):
    initial_state = []
    #position of each plane
    position = ['None' for x in range(len(planes))]
    #time in minutes for each plane
    time = [0 for x in range(len(planes))]
    #List of flights for each plane
    flights = [tuple([]) for x in range(len(planes))]
    #Defines the initial state
    initial_state = (tuple(position), tuple(time), tuple(flights), 0)
    return initial_state

####         Converts state to list             #######
def state_to_list(state):
    state_list = list((list(state[0]), list(state[1]), list([list(x) for x in state[2]]),state[3]))
    return state_list

def state_to_tuple(state):
    state_tuple = tuple((tuple(state[0]), tuple(state[1]), tuple([tuple(x) for x in state[2]]),state[3]))
    return state_tuple

#####       Converts time from 00h00m to m      ######
def minute_converter(time):
    hour = int(time[:2])
    minute = int(time[-2:])
    time_minutes = hour*60+minute
    return time_minutes

####         Converts Time back to 00h00m       ######
def hour_converter(time):
    hour = int(time/60)
    minutes = time-hour*60;
    if hour<10:
        hour = '0'+str(hour)
    if minutes<10:
        minutes = '0'+str(minutes)
    time = str(hour)+str(minutes)
    return time
