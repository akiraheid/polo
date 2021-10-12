Server that manages tracking the IP address of registered users.

User sends an HTTP POST to this server with the user's token and this server will log the sender's IP. Scripts on reverse proxy servers can then use this information to configure the reverse proxy to redirect to dynamic IP addresses.

# Usage

## Register a user

Run the `register` command with the `username` to register and copy the generated token. The token won't be printed again, so don't lose it!

```bash
polo add username
```

## Reset a user token

The token is only printed once and the server only stores the hashed version! Don't lose the token!

```bash
polo reset username
```

## Start server

```bash
polo start
```

There is a default salt used if none is specified to make testing/trying easier, but it's recommended to avoid using the default salt because
1. It can change at any time
1. It's not a very secure salt
