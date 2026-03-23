# SecureAPI
<img width="1155" height="713" alt="image" src="https://github.com/user-attachments/assets/688392ed-fde3-4f03-a417-c19cc8ac3eb8" />
https://pypi.org/project/secureapi/

SecureAPI is a Python API authorization library that works with any framework.
It provides a centralized and reusable way to enforce access control, prevent ID tampering, and standardize authorization logic across applications.

---

# Overview

Modern APIs often suffer from inconsistent authorization logic. Developers typically implement access checks manually in each endpoint, which leads to:

* Repeated code
* Security gaps
* Broken object-level authorization (BOLA)
* ID tampering vulnerabilities

SecureAPI solves this by introducing a unified authorization engine that can be integrated into any Python-based backend.

---

# Key Features

* Centralized authorization engine
* Role-based and ownership-based access control
* Protection against ID tampering
* Framework-agnostic design
* Works with Django, FastAPI, and Flask
* No mandatory configuration files
* Fully customizable via resolvers
* Minimal integration effort

---

# Installation

```bash
pip install secureapi
```

---

# Core Concepts

## Resource

A resource represents any entity in your system.

Examples:

* user
* order
* document
* project

---

## Action

| HTTP Method | Action |
| ----------- | ------ |
| GET         | read   |
| POST        | create |
| PUT/PATCH   | update |
| DELETE      | delete |

---

## Context

SecureAPI evaluates access using a context object:

```python
RequestContext(
    user=<authenticated_user>,
    resource="resource_name",
    action="read",
    resource_id=<resource_id>,
    tenant_id=None
)
```

---

# How It Works

When authorization is triggered, SecureAPI performs:

1. Role resolution
2. Resource fetching
3. Ownership validation
4. Access decision

If access is not allowed, an exception is raised.

---

# Implementation Guide (Industry Standard Example)

This section demonstrates how to integrate SecureAPI into a typical backend system using a **Document Management API**.

---

## Example Use Case

You have a system where:

* Users can view documents
* Only owners or collaborators can access a document
* Admins can access all documents

---

## Step 1: Define Your Model (Example)

```python
class Document:
    def __init__(self, id, owner_id, collaborators):
        self.id = id
        self.owner_id = owner_id
        self.collaborators = collaborators
```

---

## Step 2: Configure SecureAPI (Resolvers)

```python
from secureapi.config.loader import get_engine

engine = get_engine()

# Role Resolver
def role_resolver(user, tenant_id=None):
    if user.is_admin:
        return "admin"
    return "user"

# Resource Resolver
DOCUMENT_DB = {
    1: Document(id=1, owner_id=10, collaborators=[20, 30]),
    2: Document(id=2, owner_id=20, collaborators=[10]),
}

def resource_resolver(resource, resource_id):
    if resource == "document":
        return DOCUMENT_DB.get(resource_id)

# Ownership Resolver
def ownership_resolver(user, obj):
    if obj.owner_id == user.id:
        return "owner"
    if user.id in obj.collaborators:
        return "collaborator"
    return "user"

# Attach resolvers
engine.role_resolver = role_resolver
engine.resource_resolver = resource_resolver
engine.ownership_resolver = ownership_resolver
```

---

## Step 3: Use in API Endpoint

```python
from secureapi.core.context import RequestContext
from secureapi.config.loader import get_engine

def get_document(request, document_id):
    engine = get_engine()

    context = RequestContext(
        user=request.user,
        resource="document",
        action="read",
        resource_id=document_id,
        tenant_id=None
    )

    try:
        engine.authorize(context)
    except Exception as e:
        return {"error": str(e)}, 403

    return {"message": "Document data returned successfully"}
```

---

## Step 4: Behavior

### Allowed Access

* Document owner
* Document collaborator
* Admin user

### Denied Access

* Any unrelated user

---

# FastAPI Example

```python
from fastapi import FastAPI, HTTPException, Depends
from secureapi.core.context import RequestContext
from secureapi.config.loader import get_engine

app = FastAPI()

def authorize(user, document_id):
    engine = get_engine()
    context = RequestContext(user, "document", "read", document_id, None)
    try:
        engine.authorize(context)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.get("/documents/{document_id}")
def get_document(document_id: int, user=Depends(get_current_user)):
    authorize(user, document_id)
    return {"message": "Access granted"}
```

---

# Flask Example

```python
from flask import Flask, request, jsonify
from secureapi.core.context import RequestContext
from secureapi.config.loader import get_engine

app = Flask(__name__)

@app.route("/documents/<int:document_id>")
def get_document(document_id):
    user = request.user
    engine = get_engine()

    context = RequestContext(user, "document", "read", document_id, None)

    try:
        engine.authorize(context)
    except Exception as e:
        return jsonify({"error": str(e)}), 403

    return jsonify({"message": "Access granted"})
```

---

# Multi-Tenant Example

```python
context = RequestContext(
    user=request.user,
    resource="document",
    action="read",
    resource_id=1,
    tenant_id=1001
)
```

Tenant validation logic can be added inside resolvers.

---

# Error Handling

```python
try:
    engine.authorize(context)
except Exception as e:
    return {"error": str(e)}, 403
```

---

# Best Practices

* Keep resolver functions efficient
* Avoid heavy database queries in resolvers
* Use consistent role naming across the system
* Always validate ownership for sensitive resources
* Centralize resolver definitions in one place

---

# Security Benefits

SecureAPI helps protect against:

* Broken Object Level Authorization (BOLA)
* ID tampering attacks
* Unauthorized resource access
* Role escalation vulnerabilities

---

# Limitations

* No built-in policy engine (planned)
* No admin UI (planned)
* Requires resolver implementation

---

# Roadmap

* Policy-based configuration (YAML / DB)
* Native DRF permission class
* Audit logging
* Threat detection mechanisms
* Admin dashboard

---

# Contributing

```bash
git clone https://github.com/vaibhavpatil007/secureapi
cd secureapi
pip install -r requirements.txt

```

---

# License

MIT License © 2026 Vaibhav Patil

---

# Summary

SecureAPI provides a structured and reusable approach to authorization in Python applications.
It eliminates repetitive security logic and ensures consistent access control across all endpoints.
