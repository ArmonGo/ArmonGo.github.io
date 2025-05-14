FROM ruby:3.2-slim

WORKDIR /srv/jekyll

# Install Bundler and the latest Jekyll
RUN gem install bundler -v 2.4.22 \
 && gem install jekyll -v '~>4.4'

# Install any plugins via Gemfile (if present)
COPY Gemfile ./
RUN bundle install || echo "No Gemfile detected, skipping bundle install"

COPY . .

# Build the site
CMD ["jekyll", "build", "--config", "_config.yml"]