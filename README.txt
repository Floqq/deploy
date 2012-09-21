Deployment program for Floqq's GAE App

Provides several programs to make the deployment procedure easier and more secure.

Programs:

floqq-export

This program all it does is export the project git repository into a tar file 
using `git archive`.


floqq-configure

This program will add the to the archive all the .yaml files and settings.py file
you say.


floqq-deploy

This program takes the project tar and deploys it to GAE.
