from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.routes import leads, interactions, templates, reminders, dashboard, integrations

# Este arquivo importa todos os blueprints para facilitar o registro
