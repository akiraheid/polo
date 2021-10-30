const fs = require("fs")
const crypto = require("crypto")
const http = require("http")

const SALT = Buffer.from("SnakeCityIjustwannatakeanotherlookatyouwillyouletme", "utf-8")
let users = {}
let ips = {}

fs.readFile("/users.txt", "utf8", function (err,data) {
	if (err) {
		return console.log(err)
	}
	let lines = data.split("\n")
	for (let i = 0; i < lines.length; ++i) {
		const line = lines[i]
		if (!line.includes(":")) {
			continue
		}

		const parts = line.split(":")
		const user = parts[0]
		const hash = parts[1]
		users[hash] = user
	}
})

function generateHash(token) {
	let byteToken = Buffer.from(token, "utf-8")
	let hmac = crypto.createHmac("sha512", byteToken)
	hmac.update(SALT)
	return hmac.digest("hex")
}

function writeIP(hash) {
	const ip = ips[hash]
	const user = users[hash]

	const fileName = `ips/${user}.txt`
	fs.writeFile(fileName, `${user}:${ip}`, (err) => {
		if (err) { console.log(err) }
	})
}

async function parseJSON(req) {
	const buffers = []

	for await (const chunk of req) {
		buffers.push(chunk)
	}

	const jsonStr = Buffer.concat(buffers).toString()
	console.log(`JSON content\n${jsonStr}`)
	return JSON.parse(jsonStr)
}

function send(res, statusCode) {
	res.writeHead(statusCode)
	res.end()
}

const requestListener = async function (req, res) {
	console.log(ips)
	if (req.method != "POST") {
		return send(res, 400)
	}

	data = await parseJSON(req)
	token = data.token
	if (token == undefined) {
		return send(res, 400)
	}

	const hashed = generateHash(token)

	user = users[hashed]
	if (user == undefined) {
		return send(res, 400)
	}

	console.log(`Authenticated ${user}`)
	console.log(req.headers)
	const forwarded = req.headers["x-forwarded-for"]
	const remoteIP = req.socket.remoteAddress
	console.log(`Forwarded headers: ${forwarded}`)
	console.log(`Remote IP: ${remoteIP}`)
	const ip = forwarded || remoteIP
	console.log(`Storing IP: ${ip}`)
	ips[hashed] = ip
	writeIP(hashed)

	send(res, 200)
}

const server = http.createServer(requestListener)
const port = 8080
console.log(`Starting server on ${port}`)
server.listen(port)
