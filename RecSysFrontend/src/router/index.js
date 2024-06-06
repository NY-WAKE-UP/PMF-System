import { createRouter, createWebHistory } from 'vue-router';
import Popular_movies from "@/components/Popular_movies.vue";
import Recommend_for_u from "@/components/Recommend_for_u.vue";
import Login from "@/components/Login.vue";
import Details from "@/components/Details.vue";
import Signup from "@/components/Signup.vue";
import Welcome from "@/components/Welcome.vue";
import Profile from "@/components/Profile.vue";
import searchResults from "@/components/searchResults.vue";
import RatedMovies from "@/components/RatedMovies.vue";
import Rating from "@/components/Rating.vue";
import GenreMovies from "@/components/GenreMovies.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            redirect: "/welcome"
        },
        {
            path: '/popular_movies',
            component: Popular_movies
        },
        {
            path: '/recommend_for_u',
            component: Recommend_for_u
        },
        {
            path: '/ratings',
            component: Rating
        },
        {
            path: "/login",
            component: Login
        },
        {
            path: '/details/:movieId',
            name: 'details',
            component: Details
        },
        {
            path: '/signup',
            component: Signup
        },
        {
            path: '/welcome',
            component: Welcome
        },
        {
            path: '/profile',
            component: Profile,
            name: 'profile'
        },
        {
            path: '/searchResults',
            component: searchResults,
            name: 'searchResults'
        },
        {
            path: '/rated',
            component: RatedMovies,
            name: 'ratedMovies'
        },
        {
            path: '/genre/:genre',
            name: 'genreMovies',
            component: GenreMovies
        }
    ]
});

export default router;
