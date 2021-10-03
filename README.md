Server that manages tracking the IP address of registered users.

User sends an HTTP POST to this server with the user's token and this server will log the sender's IP. Scripts on reverse proxy servers can then use this information to configure the reverse proxy to redirect to dynamic IP addresses.

# Usage

## Register a user

Run the `register` command with the `username` to register and copy the generated token. The token won't be printed again, so don't lose it!

```bash
polo register username
```

## Reset a user token

The token is only printed once and the server only stores the hashed version! Don't lose the token!

```bash
polo reset username
```

## Start server

```bash
polo start [salt]
```
