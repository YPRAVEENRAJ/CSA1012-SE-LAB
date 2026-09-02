# Step 1: Use official Nginx Alpine image for lightweight footprint
FROM nginx:alpine

# Step 2: Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Step 3: Copy custom static website files to Nginx web root
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY script.js /usr/share/nginx/html/

# Step 4: Expose Port 80
EXPOSE 80

# Step 5: Start Nginx web server in foreground mode
CMD ["nginx", "-g", "daemon off;"]
