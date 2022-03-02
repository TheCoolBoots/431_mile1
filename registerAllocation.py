import re


class GraphNode:
    None


class GraphNode:
    def __init__(self, id: str, edges: dict[str: GraphNode], ranges: list[tuple[int, int]], color: int) -> None:
        self.id = id
        self.edges = edges
        self.ranges = ranges
        self.color = color


class Graph:
    def __init__(self, nodes:list[GraphNode]) -> None:
        self.nodes = nodes



# take in the arm code as a list (ssa registers) and convert to only have numRegisters
def allocateRegisters(armCode: list[str], numRegisters: int) -> list[str]:


    # compute live ranges for each temporary value
        # make a range of line numbers that each register is used
    liveRange = computeLiveRange(armCode)
    print(str(liveRange))





    # construct interference graph
        # edges represent interference
    # nodeGraph = createGraph(liveRange)

    # liveRange = {'%t3': [(1, 2)], '%t4': [(1, 1), (4, 5)], '%t1': [(6, 7)], '%t2': [(4, 7)]}

# PLEASE NOTE: IN ORDER TO MAKE THIS FUNCTION WORK, YOU WILL NEED TO MAKE THE LIVE RANGE TUPLE INTO A LIST
# YOU WILL ALSO EVENTUALLY NEED TO CONSIDER store AND load FOR THE END OF ONE RANGE AND START OF ANOTHER
    nodeGraph, nodeDict = createGraphV2(liveRange, len(armCode))


    # print(str(nodeGraph.nodes))

    # for node in nodeGraph.nodes:
    #     print("currNode is " + str(node.id))
    #     for nodeId in node.edges:
    #         print('\tedge node id: ' + str(nodeId))
    #
    #     print('\n')




    # color the graph with n colors
        # each color is a register
        # no adjacent nodes may hold the same color
        # prioritize the lower 'number' colors
    coloredGraph = colorizeGraph(nodeGraph, numRegisters, nodeDict)


    for node in coloredGraph.nodes:
        print("currNode is " + str(node.id))
        print('currNode color is: ' + str(node.color))
        print('\n')


    # finally, step back through the arm code and change all the registers to the colors


    # WRITE CODE HERE



# GARBAGE RETURN
    return None




# walk through each line and find the registers that are used split on % and then split each list on space
def computeLiveRange(armCode: list[str]) -> dict[str : list[tuple[int, int]]]:
    registerDict = {}
    lineNum = 1 # we dont really start at 1 tho do we


# WE WILL NEED TO HAVE A SPECIAL CASE FOR load AND store


    # step through each line of Arm code
    for line in armCode:

        # regular expression for 1 or more numbers
        p = re.compile('%t\d+')

        # MIGHT WANT TO CONSIDER SKIPPING OVER COMMENTS (they start with @)

        # split the expression on spaces
        exps = line.split(' ')

        # step through each expression to see if it has a register at the start
        for exp in exps:

            # check if we have a match, should return a list of matches (the actual numbers)
            currMatch = p.findall(exp)

            # step through each item in the matched register list
            for num in currMatch:
                registerDict = extendLiveRange(num, registerDict, lineNum)

        lineNum += 1


    for key in registerDict:
        registerDict[key] = [registerDict[key]]

    return registerDict





def extendLiveRange(num: int, registerDict: dict[str : list[tuple[int, int]]], lineNum: int) -> dict[str : list[tuple[int, int]]]:
    # if the number is already in the dict ...
    if num in registerDict:
        # update the end of the live range of the num
        registerDict[num] = (registerDict[num][0], lineNum)

    # the number isnt in the dictionary, we must add it
    else:
        # update the start and end of the live range to be at the same spot
        registerDict[num] = (lineNum, lineNum)

    return registerDict




def createGraph(nodes: dict[str : tuple[int, int]]) -> Graph:
    finalGraph = Graph([])

    # create a graph node for each node in the dict
    for node in nodes:
        # add each node to the graph
        finalGraph.nodes.append(GraphNode(node, {}, nodes[node][0], nodes[node][1], -1))

    for currNode in finalGraph.nodes:
        for tempNode in finalGraph.nodes:
            if currNode.id == tempNode.id:
                continue

            # edges overlap
            # if (end is between start and end inclusive) or (start is between start and end inclusive)
            if (currNode.end <= tempNode.end and currNode.end >= tempNode.start) or (currNode.start <= tempNode.end and currNode.start >= tempNode.start):
                # add the node to the edge list for each
                currNode.edges[tempNode.id] = tempNode
                tempNode.edges[currNode.id] = currNode

    return finalGraph




# the idea is that we will instead figure out which graph is located at each lineNum and create the graph using that information
def createGraphV2(nodes: dict[str : list[tuple[int, int]]], numberOfLines: int) -> Graph:

    # ALTHOUGH I THINK THIS SOLUTION WOULD WORK, IT WOULD BE DUMB SLOW.

    # lineCounter = 1
    # lineDict = {}
    # # look at each line
    # while lineCounter <= numberOfLines:
    #     lineDict[lineCounter] = []
    #     # for each node
    #     for node in nodes:
    #         ranges = nodes[node]
    #         # look at all the ranges for that node
    #         for range in ranges:
    #             # check if the line is within the range
    #             if(lineCounter <= range[1] and lineCounter >= range[1]):
    #                 # UPDATE lineDict WITH CURRENT NODE ID
    #                 lineDict[lineCounter] = lineDict[lineCounter].append(node)
    #                 break
    #
    #
    #     lineCounter += 1


    # ALTERNATE SOLUTION

    # It may be faster to look at the ranges of each node individually and insert into the
    # lineDict that way. This way we only have to look into each dictionary once
    lineDict = {}
    counter = 1
    while counter <= numberOfLines:
        lineDict[counter] = []
        counter += 1

    for node in nodes:
        ranges = nodes[node]
        # look at all the ranges for that node
        for range in ranges:
            start = range[0]
            end = range[1]
            while start <= end:
                # print(start)
                lineDict[start].append(node)
                # print(lineDict[start])
                start += 1

    nodeDict = {}
    # create the nodes
    for node in nodes:
        currNode = GraphNode(node, {}, [(nodes[node][0][0], nodes[node][0][1])], -1)

        if(len(nodes[node]) > 1):
            count = 1
            while count < len(nodes[node]):
                currNode.ranges.append((nodes[node][count][0], nodes[node][count][1]))
                count += 1

        nodeDict[node] = currNode


    # now step thru lineDict and create the graph
    for lineNum in lineDict:
        nodes = lineDict[lineNum]
        # step thru each node and add the others to the edge list
        for nodeId in nodes:
            for otherId in nodes:
                if nodeId == otherId:
                    continue
                nodeDict[nodeId].edges[otherId] = nodeDict[otherId]


    returnGraph = Graph([])
    for nodeId in nodeDict:
        returnGraph.nodes.append(nodeDict[nodeId])

    return returnGraph, nodeDict
            # if(lineCounter <= range[1] and lineCounter >= range[1]):






def colorizeGraph(graph: Graph, numColors: int, nodeDict: dict[str : GraphNode]) -> Graph:

    mostEdges = -1
    initialNode = None
    # start with node that has the most edges (highest degree), put it onto the stack
    for node in graph.nodes:
        if len(node.edges) >  mostEdges:
            mostEdges = len(node.edges)
            initialNode = node

    nodeStack = [initialNode]

    while(True):
        graph = colorHelper(graph, nodeStack, numColors, nodeDict)

        # if all nodes have been colored, we can return
        coloredFlag = True
        for node in graph.nodes:
            if node.color == -1:
                coloredFlag = False
                nodeStack = [node]
                break

        if(coloredFlag):
            return graph



def colorHelper(graph: Graph, nodeStack: list[GraphNode], numColors: int, nodeDict: dict[str : GraphNode]) -> Graph:

    nodeDict = {}

    # loop until the stack is empty
    while nodeStack != []:
        currNode = nodeStack.pop(0)

        # make sure the currNode isnt in the nodeDict (already seen)
        if currNode in nodeDict:
            continue

        colorList = [x for x in range(1, numColors + 1)]

        # when looking at a node see if any of the edges have color 1->numColors
        for tempNodeId in currNode.edges:
            # the node is colored, make sure the currNode doesnt copy this color
            if currNode.edges[tempNodeId].color != -1:
                # print("edge id: " + str(tempNodeId))
                # print("edge color: " + str(currNode.edges[tempNodeId].color))
                colorList.remove(currNode.edges[tempNodeId].color)
            # the node is not colored, add it to the stack so it gets colored
            else:
                nodeStack.append(currNode.edges[tempNodeId])

        # assign it the smallest color that isn't in use
        # THIS IS THE SPECIAL CASE FOR WHEN WE ARE OUT OF COLORS - YOU WILL NEED TO CHANGE THE ARM CODE TO store AND load
        if len(colorList) == 0:
            print("YOU HIT THE SPECIAL CASE, YOU'VE RUN OUT OF COLORS.")


            # WRITE CODE


        else:
            currNode.color = colorList[0]


        # put the current node into a dictionary so that you dont try to color it again
        nodeDict[currNode] = True

    return graph



    # now that the stack is empty, loop through the graph nodes and make sure they all have color

    # if a node doesn't have color, put it on the stack and run again until stack is empty
        # repeat this process until every node has color





    return graph




def main():

    armCode = [
    'and %t3, %t4, #1', # line 1
    'cmp %t3, #1',
    'bne continue',
    'mov %t1, %t2',
    'mov %t2, %t3',
    'bl intadd',
    'mov %t2, %t1'] # line 7

    # liveRange = computeLiveRange(armCode)

    # print(str(liveRange))


    allocateRegisters(armCode, 10)



if __name__ == "__main__":
    main()
