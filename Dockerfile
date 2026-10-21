# AstronomicAL with the astro-science portfolio plugin
FROM python:3.12-slim

WORKDIR /app

# System deps for scientific Python wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# uv for fast, reproducible installs
RUN pip install --no-cache-dir uv

# Copy the AstronomicAL source
COPY . /app

# Create venv and install deps (deliberate pandas/numpy upgrade: drop sparclclient pin)
RUN rm -rf /app/.venv && uv venv --python 3.12 /app/.venv && \
    uv pip install --python /app/.venv/bin/python \
        -r requirements-core.txt -r requirements-astro.txt -r requirements-ml.txt && \
    uv pip uninstall --python /app/.venv/bin/python sparclclient && \
    uv pip install --python /app/.venv/bin/python --upgrade "pandas>=2.2" "numpy>=2" "pyarrow>=24" "scikit-learn>=1.2"

# Install the portfolio plugin (bundled location so it is auto-discovered)
RUN mkdir -p /app/astronomicAL/plugins/astro_science_portfolio && \
    cp /app/custom_plugins/astro_science_portfolio/* /app/astronomicAL/plugins/astro_science_portfolio/

# Pre-enable the portfolio plugin (user plugin roots are not auto-enabled)
RUN mkdir -p /root/.astronomical && \
    printf '%s\n' '{ "schema_version": 1, "community_plugins_enabled": true, "plugins": { "astro.science.portfolio": { "enabled": true } } }' > /root/.astronomical/plugin-state.json

# The plugin reads research data from /data (mounted at runtime)
ENV ASTRO_SCIENCE_ROOT=/data

EXPOSE 8080

# Default: serve the app on 0.0.0.0:8080
CMD ["/app/.venv/bin/python", "-m", "panel", "serve", "astronomicAL", \
     "--port", "8080", "--address", "0.0.0.0", \
     "--allow-websocket-origin", "*"]
