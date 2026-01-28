#Pablo Urbina Macip
#Practica Flask: Desarrollar una aplicacion web monolitica con flask (Frontedn con Jinja) que implemente un crud completo para la entidad Producto, incluyendo un login ficticio con sesion y persistencia en SQLite.
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3