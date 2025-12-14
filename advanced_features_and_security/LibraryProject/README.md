This is my LibraryProject built with Django

# Permissions and Groups Setup 

## Custom Permissions
The `book` model includes the following custom permissions : 
- `can_view`
- `can_create`
- `can_edit`
- `can_delete`

these are defined in `bookshelf/models.py`

## Groups 
Three Groups were created in Django admin :

### Viewers 
- can_view

### Editors
- can_view
- can_create
- can_edit

### Admins 
- can_view
- can_create
- can_edit
- can_delete

### Views Permission Enforcement 
Views in `bookshelf/views.py` are protected using `@permission_required`.

Examples:
```python
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    ...
