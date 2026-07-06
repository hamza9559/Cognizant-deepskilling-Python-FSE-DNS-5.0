import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class CourseService {

  constructor(private http: HttpClient) { }

  getCourses(): Observable<any[]> {
    return this.http.get<any[]>('https://jsonplaceholder.typicode.com/posts?_limit=5').pipe(
      map(posts => posts.map(post => ({
        id: post.id,
        name: post.title.split(' ').map((w: string) => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
        code: `CS${100 + post.id * 5}`,
        credits: (post.id % 2) + 3, // alternating 3 and 4 credits
        grade: post.id % 3 === 0 ? 'A' : (post.id % 3 === 1 ? 'A-' : 'B+')
      })))
    );
  }
}
