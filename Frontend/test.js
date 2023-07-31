const headers = new Headers()
headers.append("Content-Type", "application/json")

const body = {
  "test": "event"
}

const options = {
  method: "POST",
  headers,
  mode: "cors",
  body: JSON.stringify(body),
}

fetch("https://eofn7ve6epuaruq.m.pipedream.net/", options)
