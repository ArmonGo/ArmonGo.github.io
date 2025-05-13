FROM ruby:2.7-slim

# Install Python + image-resize & CSS deps
RUN apt-get update && \
    apt-get install -y \
      python3 \
      python3-libsass \
      python3-rcssmin \
      python3-pil \
      build-essential \
      libjpeg-dev \
      zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /srv/jekyll

# Update RubyGems, install ffi, then Bundler and Jekyll
RUN gem update --system 3.3.22 \
 && gem install ffi -v 1.17.2 \
 && gem install bundler -v 2.4.22 \
 && gem install jekyll -v "~>2.5"

# Install any plugins via Gemfile (if present)
COPY Gemfile ./
RUN bundle install || echo "No Gemfile detected, skipping bundle install"

# Copy the rest of your site + build script
COPY . .

# Entry point: runs your Python build script (SCSS, thumbnails, then Jekyll)
CMD ["python3", "build.py"]
