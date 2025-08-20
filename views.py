
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Seat
from .forms import MovieForm

# List all movies
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movieticket/movie_list.html', {'movies': movies})

# Add new movie and auto-create seats
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            # ✅ Ensure seats are created only once per movie
            if not Seat.objects.filter(movie=movie).exists():
                create_seats_for_movie(movie)
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'movieticket/add_movie.html', {'form': form})
  
def book_ticket(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        num_seats = int(request.POST.get('seats'))
        request.session['num_seats'] = num_seats
        return redirect('book_seats', movie_id=movie.id)

    return render(request, 'movieticket/book_ticket.html', {'movie': movie})

def create_seats_for_movie(movie):
    rows = "ABCDEFGHIJ"  # 10 rows
    for r in rows:
        for n in range(1, 11):  # 10 seats per row
            seat_number = f"{r}{n}"
            if r in "AB":
                price = 300
            elif r in "CD":
                price = 200
            else:
                price = 100
            Seat.objects.create(
                movie=movie,
                seat_number=seat_number,
                price=price,
                is_booked=False
            )

def book_seats(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if not movie.seats.exists():
        create_seats_for_movie(movie)

    seats = movie.seats.all().order_by('seat_number')
    grid = [seats[i:i+10] for i in range(0, len(seats), 10)]

    if request.method == "POST":
        selected_seat_ids = request.POST.getlist('seats')
        if not selected_seat_ids:
            error = "Please select at least one seat."
            return render(
                request,
                'movieticket/book_seats.html',
                {'movie': movie, 'grid': grid, 'error': error}
            )

        booked_seats = Seat.objects.filter(id__in=selected_seat_ids)
        booked_seats.update(is_booked=True)
        return render(
            request,
            'movieticket/booking_success.html',
            {'movie': movie, 'booked_seats': booked_seats}
        )

    return render(request, 'movieticket/book_seats.html', {'movie': movie, 'grid': grid})
