const express = require('express');
const { WebSocketServer } = require('ws')
const dir = `${__dirname}/public/`;
const { spawn } = require('child_process');
const webserver = express()
    
webserver.get("/", (req, res) => {
  res.sendFile(dir + "capHome.html");
});
webserver.get("/queue.html", (req, res) => {
  res.sendFile(dir + "queue.html");
});
webserver.get("/private.html", (req, res) => {
    res.sendFile(dir + "private.html");
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
let clientDict = new Map() // key: clientID, value: websocket
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
        clientDict.get(clientID).send(fmsg)
    }else{
        console.log("error: Client " + clientID + "does not exist")
    }
}

//example things for working with child processes
child = spawn('python3', ["test.py","./"])
var res = '';
child.stdout.on('data', function (_data) {
    try {
        var data = Buffer.from(_data, 'utf-8').toString();
        res += data;
    } catch (error) {
        console.error(error);
    }
    console.log(res)
});
child.stdin.setEncoding('utf-8');
child.stdin.write(" you it worked" + '\r\n');
child.stdin.end();


//private matchmaking
wss2.on('connection', ws => {
    let self = 0;
    let clientID = clientIDcounter++;
    let lobbyID = -1;
    let oppID = -1;
    let un = ["fighter", "fighter", "tanker", "bomber", "jammer", "C2"]

    clientDict.set(clientID, ws) //create entry in clientDictionary
    console.log('New client ' + clientID + ' connected!')
    //clientDict.get(clientID).send('connection established')
    
    ws.on('message', data => {
        const msg = JSON.parse(data);
        switch (msg.type) {
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
                oppID = -1
                lobbyDict.get(lobbyID)[1] = clientID
                lobbyDict.get(lobbyID)[2] = null
                lobbyDict.get(lobbyID)[3] = null
            break;
            case "autojoin":
                for(let i = 0; i < queueLobbies; i++){
                    if(lobbyDict.get(i)[0] == "waiting"){
                        self = 2
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
                        self = 2
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
            case "unit":
                unit = msg.text
                let found = false
                myunits = queue_units.get(lobbyID)[self-1]
                for (let i = 0; i < myunits.length; i++) {
                    if(myunits[i] == unit){
                        found = true
                        myunits.splice(i,1)
                    }
                  }
                if(found == false){
                    msg.text = `You cannot generate another ${unit}`
                    console.log(`Player ${self} tried to generate a ${unit}`)
                    generated = JSON.stringify(msg);
                    ws.send(generated)
                }
                else{
                    msg.text = `Player ${self} generated a ${unit}`
                    console.log(`Player ${self} generated a ${unit}`)
                    generated = JSON.stringify(msg);
                    opp.send(generated)
                    msg.text = `You generated a ${unit}`
                    generated = JSON.stringify(msg);
                    ws.send(generated)
                    msg.text = `You can still generate: ${myunits}`
                    generated = JSON.stringify(msg);
                    ws.send(generated)
                }
            break;
            case "roll":
                if(self % 2 == 1){
                    even = false;
                }else{
                    even = true;
                }
                if((even && rolls.even != -1) || (!even && rolls.odd != -1)){
                    console.log(`Player ${self} tried to roll again`)
                    sendMessage(clientID, "roll", "You already rolled.")
                }
                else{
                    roll = msg.text
                    if(even){
                        rolls.even = roll;
                    }else{
                        rolls.odd = roll;
                    }
                    console.log(`Player ${self} rolled a ${roll}`)
                    sendMessage(oppID, "roll", `Player ${self} rolled a ${roll}`)
                    sendMessage(clientID, "roll", `You rolled a ${roll}`)
                }
            break;
        }
        if(rolls.even != -1 && rolls.odd != -1){ //handle rolls after a turn
            let higher = -1
            let roller = -1
            if(rolls.even > rolls.odd){
               higher = rolls.even
               if(even){
                roller = self
               }
               else{
                if(self == 1){roller = 2}else{roller = 1}
               }
            }
            else{
                higher = rolls.odd
                if(even){
                    if(self == 1){roller = 2}else{roller = 1}
                   }
                else{
                    roller = self
                }
            }
            sendMessage(clientID, "roll", `The higher roll was ${higher} by Player ${roller}`)
            sendMessage(oppID, "roll", `The higher roll was ${higher} by Player ${roller}`)
            //in the future this reset will happen after both turns to prevent rolling in the middle of a turn
            rolls.even = -1
            rolls.odd = -1
           }
       })

    ws.on('close', () => {
        if(oppID != -1){
            sendMessage(oppID, "left", " ")
            console.log(lobbyID + ": Player " + self + "has left the lobby")
        }else if (lobbyID != -1){
            if(lobbyDict.get(lobbyID)[0] == "waiting"){
                lobbyDict.get(lobbyID)[0] = "empty"
                lobbyDict.get(lobbyID)[3] = null
            }else if(lobbyDict.get(lobbyID)[0] == "open"){
                lobbyDict.delete(lobbyID)
            }
        }
        clientDict.delete(clientID)
        console.log(clientID + ' has disconnected!')
    })
    ws.onerror = function () {
        console.log('websocket error')
    }
})
