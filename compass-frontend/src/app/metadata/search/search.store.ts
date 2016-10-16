import { Injectable } from '@angular/core';

import 'rxjs/add/operator/toPromise';

import {BehaviorSubject} from "rxjs/Rx";

import {SearchParameters} from "./search-parameters";
import {SearchResult} from "./search-result";
import {SearchService} from "./search.service";


@Injectable()
export class SearchStore {
  private _searchResults: BehaviorSubject<SearchResult[]> = new BehaviorSubject([]);
  private _autocompleteSearchResults: BehaviorSubject<SearchResult[]> = new BehaviorSubject([]);
  private _count: BehaviorSubject<number> = new BehaviorSubject(0);
  private _next: BehaviorSubject<URL> = new BehaviorSubject(null);
  private _previous: BehaviorSubject<URL> = new BehaviorSubject(null);

  constructor(private searchService: SearchService) {
    this.search(new SearchParameters());
  }

  get searchResults() {
    return this._searchResults.asObservable();
  }

  get autocompleteSearchResults() {
    return this._autocompleteSearchResults.asObservable();
  }

  get count() {
    return this._count.asObservable();
  }

  get next() {
    return this._next.asObservable();
  }

  get previous() {
    return this._previous.asObservable();
  }

  autocomplete(params: SearchParameters) {
    let obs = this.searchService.getSearchResultList(params);
    obs.subscribe(
      res => {
        let results = res.json();
        let searchResults = <SearchResult[]>results["results"];
        if (searchResults.length > 0) {
          this._autocompleteSearchResults.next(searchResults);
        }
      },
      err => console.log("Error retrieving...")
    );
  }


  search(params: SearchParameters) {
    let obs = this.searchService.getSearchResultList(params);

    obs.subscribe(
        res => {
          let results = res.json();
          let searchResults = <SearchResult[]>results["results"];
          let count = <number>results["count"];
          let next = results["next"];
          let previous = results["previous"];
          this._searchResults.next(searchResults);
          this._count.next(count);
          this._next.next(next);
          this._previous.next(previous);
        },
        err => console.log("Error retrieving...")
    );
  }
}
