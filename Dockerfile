FROM ruby:3.2-slim

# Install build tools for native gems
RUN apt-get update && \
    apt-get install -y \
      build-essential \
      libffi-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /srv/jekyll

# Install Bundler and Jekyll
RUN gem install bundler -v 2.4.22 \
 && gem install jekyll -v '~>4.4'

# Install any plugins via Gemfile (if present)
# COPY Gemfile ./
# RUN bundle install || echo "No Gemfile detected, skipping bundle install"

# Copy your site source in
COPY . .

# Build the site
CMD ["jekyll", "build", "--trace", "--config", "_config.yml"]
