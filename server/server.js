const express = require('express');
const { WebSocketServer } = require('ws')
const dir = `${__dirname}/public/`;
const { spawn } = require('child_process');
const webserver = express()
webserver.use("/public", express.static("back3.gif"));

webserver.get("/", (req, res) => {
  res.sendFile(dir + "capHome.html");
});
webserver.get("/queue.html", (req, res) => {
  res.sendFile(dir + "queue.html");
});
webserver.get("/private.html", (req, res) => {
    res.sendFile(dir + "private.html");
  });
webserver.get("/hex.css", (req, res) => {
    res.sendFile(dir + "hex.css");
  });
webserver.get("/back.css", (req, res) => {
    res.sendFile(dir + "back.css");
  });
webserver.get("/mod.css", (req, res) => {
    res.sendFile(dir + "mod.css");
  });
webserver.get("/bluecarrier.png", (req, res) => {
    res.sendFile(dir + "bluecarrier.png");
  });
webserver.get("/p1bomber.png", (req, res) => {
    res.sendFile(dir + "p1bomber.png");
  });
webserver.get("/p2bomber.png", (req, res) => {
    res.sendFile(dir + "p2bomber.png");
  });
webserver.get("/p1tanker.png", (req, res) => {
    res.sendFile(dir + "p1tanker.png");
  });
webserver.get("/p2tanker.png", (req, res) => {
    res.sendFile(dir + "p2tanker.png");
  });
webserver.get("/p1fighter1.png", (req, res) => {
    res.sendFile(dir + "p1fighter1.png");
  });
webserver.get("/p1fighter2.png", (req, res) => {
    res.sendFile(dir + "p1fighter2.png");
  });
webserver.get("/p2fighter1.png", (req, res) => {
    res.sendFile(dir + "p2fighter1.png");
  });
webserver.get("/p2fighter2.png", (req, res) => {
    res.sendFile(dir + "p2fighter2.png");
  });
webserver.get("/p1jammer.png", (req, res) => {
    res.sendFile(dir + "p1jammer.png");
  });
webserver.get("/p2jammer.png", (req, res) => {
    res.sendFile(dir + "p2jammer.png");
  });
webserver.get("/p1comms.png", (req, res) => {
    res.sendFile(dir + "p1comms.png");
  });
webserver.get("/p2comms.png", (req, res) => {
    res.sendFile(dir + "p2comms.png");
  });
webserver.get("/numbers.jpg", (req, res) => {
res.sendFile(dir + "numbers.jpg");
});
webserver.get("/units.jpg", (req, res) => {
res.sendFile(dir + "units.jpg");
 });

// Serve a 404 page on all other accessed routes, or redirect to specific page
webserver.get("*", (req, res) => {
    res.redirect("/");
});
webserver.listen(8080, () => console.log(`Listening on ${8080}`))

const wss2 = new WebSocketServer({ port: 8082 })

//functions for rolls
let rolls = {
    even: -1,
    odd: -1,
  };
let even = false;

//structures for game
let clientIDcounter = 0;
let lobbyDict = new Map() //(lobby ID: [empty/waiting/full/open/closed, clientID(player 1), clientID(player 2), process])
let clientDict = new Map() // key: clientID, value: [websocket, bool endTurn, string turnMove]
let queueLobbies = 100;

for(let i = 0; i < queueLobbies; i++){ //create queueLobbies number of empty lobbies
    lobbyDict.set(i, ["empty", null, null, null])
}

function sendMessage(clientID, type, text){
    const msg = {type:"", text:"",}
    msg.type = type
    msg.text = text
    fmsg = JSON.stringify(msg)
    if(clientDict.has(clientID)){
        clientDict.get(clientID)[0].send(fmsg)
    }else{
        console.log("error: Client " + clientID + "does not exist")
    }
}

//private matchmaking
wss2.on('connection', ws => {
    let self = 0;
    let clientID = clientIDcounter++;
    let lobbyID = -1;
    let oppID = -1;
    let un = ["fighter1", "fighter2", "tanker", "bomber", "jammer", "C2"]

    clientDict.set(clientID, [ws, false, null]) //create entry in clientDictionary
    console.log('New client ' + clientID + ' connected!')
    //clientDict.get(clientID).send('connection established')

    ws.on('message', data => {
        const msg = JSON.parse(data);
        switch (msg.type) { //handles messages sent to the websocket
            //lobby set up
            case "create":
                lobbyID = String((Math.floor(100000 + Math.random() * 900000))) //ensures a six digit number
                if(lobbyDict.has(lobbyID)){ //in case it regenerates an ID that is being used, will retry until unique
                    while(private_list.has(lobbyID)){
                        lobbyID = String((Math.floor(100000 + Math.random() * 900000)))
                    }
                }
                lobbyDict.set(lobbyID, ["open", clientID, null, null]) //create entry in lobbyID dictionary, with null placeholders
                //queue_units.set(lobbyID, [un, null])
                self = 1
                sendMessage(clientID, "created", lobbyID) //return lobbyID to client
                sendMessage(clientID, "player-num", "blue");
                console.log("--Client " + clientID + ": created lobby " + lobbyID) //success message to console
            break;
            case "join":
                lobbyID = msg.text
                if(lobbyDict.has(lobbyID)){
                    lobbyInfo = lobbyDict.get(lobbyID)
                    if (lobbyInfo[0] == "open"){
                        self = 2
                        //queue_units.get(lobbyID)[1] = un
                        oppID = lobbyInfo[1] //remember opponentID
                        lobbyDict.get(lobbyID)[2] = clientID //set player2 in lobby to this clientID
                        sendMessage(clientID, "joined", lobbyID) //send success message to client
                        sendMessage(clientID, "player-num", "red");
                        console.log("--Client " + clientID + ": joined lobby " + lobbyID) //success message to console
                        sendMessage(oppID, "opp", clientID) //tell other player CID of their opponent
                    }
                    else{
                      sendMessage(clientID, message, "lobby full")
                    }
                }
            break;
            case "opp": //opponent joined lobby, start the process
                console.log(lobbyID + ": Player 1 received join noti")
                oppID = lobbyDict.get(lobbyID)[2]
                console.log(lobbyID + ": opp joined lobby " + lobbyID)
                lobbyDict.get(lobbyID)[3] = spawn('python3', ["test.py","./"])
                lobbyDict.get(lobbyID)[4] = 'output:'; //output string
                lobbyDict.get(lobbyID)[3].stdout.on('data', function (_data) {
                    //where we need to process python output and send to html
                    try {
                        var data = Buffer.from(_data, 'utf-8').toString();
                        lobbyDict.get(lobbyID)[4] = data;
                    } catch (error) {
                        console.error(error);
                    }
                    console.log("//////" + lobbyDict.get(lobbyID)[4])
                    var result = lobbyDict.get(lobbyID)[4].split(':');
                    var full = lobbyDict.get(lobbyID)[4];
                    console.log(result)
                    for(let i = 0; i < result.length; i++){
                        if(result[i].includes("end")){
                            sendMessage(lobbyDict.get(lobbyID)[1], "turn-result", result[i+1])
                            sendMessage(lobbyDict.get(lobbyID)[2], "turn-result", result[i+1])
                        }
                        if(result[i].includes("combat")){
                            player = result[i+1].split(',');
                            console.log(result[i+1]);
                            console.log("Me:" + self);
                            if(parseInt(player[1].charAt(0))==1){
                                sendMessage(lobbyDict.get(lobbyID)[1], "combat", result[i+1]);
                            }
                            else{
                                console.log("for whatever reason");
                                sendMessage(lobbyDict.get(lobbyID)[2], "combat", result[i+1]);
                            }
                        }
                        if(result[i].includes("evade")){
                            console.log(result[i+1]);
                            console.log("self",self);
                            if(parseInt(player[1].charAt(0))==1){
                                sendMessage(lobbyDict.get(lobbyID)[2], "evade", result[i+1])
                            }
                            if(parseInt(player[1].charAt(0))==2){
                                sendMessage(lobbyDict.get(lobbyID)[1], "evade", result[i+1])
                            }
                        }
                        if(result[i].includes("dodge")){
                            if(parseInt(player[1].charAt(0))==1){
                                sendMessage(lobbyDict.get(lobbyID)[2], "dodge", result[i+1])
                            }
                            if(parseInt(player[1].charAt(0))==2){
                                sendMessage(lobbyDict.get(lobbyID)[1], "dodge", result[i+1])
                            }
                        }
                        if(result[i].includes("feedback")){
                            sendMessage(lobbyDict.get(lobbyID)[1], "feedback", result[i+1])
                            sendMessage(lobbyDict.get(lobbyID)[2], "feedback", result[i+1])
                        }
                    }

                    console.log("result:", result)
                    if(full.includes("victor")){
                      console.log("winning")
                      winner = result[2]
                      console.log(winner)
                      sendMessage(lobbyDict.get(lobbyID)[1], "victor", result[2])
                      sendMessage(lobbyDict.get(lobbyID)[2], "victor", result[2])
                    }

                    // if(lobbyDict.get(lobbyID)[4] == "start of turn\n"){ //start turn
                    //     //send start message to both players
                    //     sendMessage(lobbyDict.get(lobbyID)[1], "start", "")
                    //     sendMessage(lobbyDict.get(lobbyID)[2],"start", "")
                    //     //print for testing
                    //     console.log(lobbyDict.get(lobbyID)[4])
                    //     console.log("sot worked")
                    // }
                });
            break;
            case "left": //opponent left lobby, reset lobby
                if(self == 2){
                    console.log(lobbyID + ": Player 1 has left the lobby")
                    sendMessage(clientID, "message", "Your opponent has left the lobby, you are now Player 1.")
                }else{
                    console.log(lobbyID + ": Player 2 has left the lobby")
                    sendMessage(clientID, "message", "Your opponent has left the lobby.")
                }
                if(lobbyDict.get(lobbyID)[0] == "closed"){
                    lobbyDict.get(lobbyID)[0] = "open"
                    sendMessage(clientID, "message", "Share your join code to start a new match.")
                }else{
                    lobbyDict.get(lobbyID)[0] = "waiting"
                    sendMessage(clientID, "message", "The next available player will be placed in your match.")
                }
                self = 1
                sendMessage(clientID, "player-num", "blue");
                oppID = -1
                lobbyDict.get(lobbyID)[1] = clientID
                lobbyDict.get(lobbyID)[2] = null
                lobbyDict.get(lobbyID)[3] = null
            break;
            case "autojoin":
                for(let i = 0; i < queueLobbies; i++){
                    if(lobbyDict.get(i)[0] == "waiting"){
                        self = 2
                        sendMessage(clientID, "player-num", "red");
                        //queue_units.get(lobbyID)[1] = un
                        lobbyID = i
                        oppID = lobbyDict.get(i)[1] //remember opponentID
                        lobbyDict.get(lobbyID)[0] = "full"
                        lobbyDict.get(lobbyID)[2] = clientID //set player2 in lobby to this clientID
                        sendMessage(clientID, "joined", lobbyID) //send success message to client
                        console.log("--Client " + clientID + ": joined lobby " + lobbyID) //success message to console
                        sendMessage(oppID, "opp", clientID) //tell other player CID of their opponent
                        break;
                    }else if(lobbyDict.get(i)[0] == "empty"){
                        self = 1
                        sendMessage(clientID, "player-num", "blue");
                        lobbyID = i
                        lobbyDict.get(lobbyID)[0] = "waiting" //mark lobby as waiting
                        lobbyDict.get(lobbyID)[1] = clientID //set player1 in lobby to this clientID
                        sendMessage(clientID, "joined", lobbyID) //send success message to client
                        console.log("--Client " + clientID + ": joined lobby " + lobbyID) //success message to console
                        break;
                    }
                }
                break;
            case "message":
                if(self == 1){
                    console.log(`distributing message from Player 1: ` + msg.text)
                    sendMessage(oppID, "message", msg.text)
                    console.log("sending ACK")
                    sendMessage(clientID, "message", "message sent")
                }
                else if(self == 2){
                    console.log(`distributing message from Player 2: ` + msg.text)
                    sendMessage(oppID, "message", msg.text)
                    console.log("sending ACK")
                    sendMessage(clientID, "message", "message sent")
                }
                else{
                    console.log("player not in lobby")
                    sendMessage(clientID, "message", "You must be in a lobby to send messages.")
                }
            break;
            case "click":
                if(self==1){
                    console.log('Player 1 clicked: ' + msg.text)
                }
                if(self==2){
                    console.log('Player 2 clicked: ' + msg.text)
                }
            break;
            //gameplay messages
            case "start":
            break;
            case "move":
                // lobbyDict.get(lobbyID)[3].stdin.setEncoding('utf-8');
                // lobbyDict.get(lobbyID)[3].stdin.cork();
                // lobbyDict.get(lobbyID)[3].stdin.write(msg.text + '\n');
                console.log(msg.text);
                // lobbyDict.get(lobbyID)[3].stdin.uncork();
            break;
            case "win":
            break;
            case "evade":
                console.log("Evading " + msg.text);
                lobbyDict.get(lobbyID)[3].stdin.cork();
                lobbyDict.get(lobbyID)[3].stdin.write(msg.text + '\n');
                lobbyDict.get(lobbyID)[3].stdin.uncork();
            break;
            case "evadeyn":
                console.log("Evading y/n " + msg.text);
                lobbyDict.get(lobbyID)[3].stdin.cork();
                lobbyDict.get(lobbyID)[3].stdin.write(msg.text + '\n');
                lobbyDict.get(lobbyID)[3].stdin.uncork();
                break;
            case "attack":
                console.log("Attacking " + msg.text);
                lobbyDict.get(lobbyID)[3].stdin.cork();
                lobbyDict.get(lobbyID)[3].stdin.write(msg.text + '\n');
                lobbyDict.get(lobbyID)[3].stdin.uncork();
            break;
            case "end of turn": //client sent that they have ended their turn and their final move, now send their moves to process
                console.log("-server recieved eot from " + clientID)
                if(clientDict.get(clientID)[1] == false){
                    clientDict.get(clientID)[1] = true
                    clientDict.get(clientID)[2] = msg.text
                }else{
                    sendMessage(clientID, "message", "You already ended your turn.")
                }
                if(clientDict.get(oppID)[1] == true){ //both players have ended their turn sosend moves in batch to server
                    lobbyDict.get(lobbyID)[3].stdin.setEncoding('utf-8');
                    lobbyDict.get(lobbyID)[3].stdin.cork();
                    if(self == 1){
                        console.log("+++" + "1,"+ clientDict.get(clientID)[2] + "?2," + clientDict.get(oppID)[2])
                        lobbyDict.get(lobbyID)[3].stdin.write("1,"+ clientDict.get(clientID)[2] + "?2," + clientDict.get(oppID)[2] + '\n');
                    }else{
                        console.log("+++" + "1,"+clientDict.get(oppID)[2] + "?2," + clientDict.get(clientID)[2])
                        lobbyDict.get(lobbyID)[3].stdin.write("1,"+clientDict.get(oppID)[2] + "?2," + clientDict.get(clientID)[2] + '\n');
                    }
                    lobbyDict.get(lobbyID)[3].stdin.uncork();
                    //reset end turn variables
                    clientDict.get(clientID)[1] = false
                    clientDict.get(oppID)[1] = false
                }
            break;
        }
       })

    ws.on('close', () => { //handles ws closure
        if(oppID != -1){ //if in lobby with another player
            sendMessage(oppID, "left", " ")
            console.log(lobbyID + ": Player " + self + "has left the lobby")
        }else if (lobbyID != -1){ //in lobby, no other player
            if(lobbyDict.get(lobbyID)[0] == "waiting"){
                lobbyDict.get(lobbyID)[0] = "empty"
                lobbyDict.get(lobbyID)[3] = null
            }else if(lobbyDict.get(lobbyID)[0] == "open"){
                lobbyDict.delete(lobbyID)
            }
        } //not in lobby, don't need to mess with lobby data structures
        clientDict.delete(clientID)
        console.log(clientID + ' has disconnected!')
    })
    ws.onerror = function () {
        console.log('websocket error')
    }
})
