FROM ghcr.io/shsridhar-beep/svgap@sha256:d800fe08199be70963965c7a0674c5f010f4bbc9bfdc129efce7bb95218ae621

# Harbor supplies its own keepalive command. Clear the SV-Gap CLI entrypoint so
# the container can accept that command and later execute agent and verifier
# processes normally.
ENTRYPOINT []
CMD ["/bin/sh"]
WORKDIR /app
