from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Subject, Note
from .forms import SubjectForm, NoteForm

@login_required
def subject_list(request):
    subjects = Subject.objects.filter(user=request.user, is_archived=False)
    return render(request, 'subjects/subject_list.html', {'subjects': subjects})

@login_required
def all_notes(request):
    notes = Note.objects.filter(subject__user=request.user)
    return render(request, 'subjects/all_notes.html', {'notes': notes})

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, subject__user=request.user)
    return render(request, 'subjects/note_detail.html', {'note': note})

@login_required
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subjects/add_subject.html', {'form': form})

@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    notes = subject.notes.all()
    
    return render(request, 'subjects/subject_detail.html', {
        'subject': subject,
        'notes': notes
    })

@login_required
def add_note(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.subject = subject 
            note.save()
            return redirect('subject_detail', subject_id=subject.id)
    else:
        form = NoteForm()
    return render(request, 'subjects/add_note.html', {'form': form, 'subject': subject})

@login_required
def search(request):
    query = request.GET.get('q', '')
    subjects = []
    notes = []
    
    if query:
        subjects = Subject.objects.filter(
            user=request.user,
            name__icontains=query
        )
        
        notes = Note.objects.filter(
            subject__user=request.user
        ).filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    return render(request, 'subjects/search_results.html', {
        'query': query,
        'subjects': subjects,
        'notes': notes,
    })

@login_required
def favorite_notes(request):
    """Exibe apenas as notas favoritas do usuário."""
    notes = Note.objects.filter(subject__user=request.user, is_favorite=True).order_by('-created_at')
    return render(request, 'subjects/favorite_notes.html', {'notes': notes})

@login_required
def archive_subject(request, subject_id):
    """Arquiva uma matéria."""
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    subject.is_archived = True
    subject.save()
    return redirect('subject_list')

@login_required
def unarchive_subject(request, subject_id):
    """Desarquiva uma matéria."""
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    subject.is_archived = False
    subject.save()
    return redirect('subject_list')

@login_required
def toggle_favorite(request, note_id):
    """Marca/desmarca uma nota como favorita."""
    note = get_object_or_404(Note, id=note_id, subject__user=request.user)
    note.is_favorite = not note.is_favorite
    note.save()
    return redirect('note_detail', note_id=note.id)

@login_required
def archived_subjects(request):
    """Exibe matérias arquivadas."""
    subjects = Subject.objects.filter(user=request.user, is_archived=True)
    return render(request, 'subjects/archived_subjects.html', {'subjects': subjects})

@login_required
def recent_notes(request):
    """Exibe notas recentes."""
    from django.utils import timezone
    import datetime
    recent_date = timezone.now() - datetime.timedelta(days=7)
    notes = Note.objects.filter(subject__user=request.user, created_at__gte=recent_date)
    return render(request, 'subjects/recent_notes.html', {'notes': notes})

