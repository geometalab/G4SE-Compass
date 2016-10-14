import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {SearchParameters} from "./search-parameters";
import {SearchStore} from "./search.store";
import {Subject, Observable} from "rxjs";
import {SearchResult} from "./search-result";


@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'],
})
export class SearchComponent implements OnInit {
  error: any;
  // pagination settings
  private itemsPerPage: number = 10;
  maxSize: number = 5; // maxNumberButtonsVisible

  private searchParams: SearchParameters = new SearchParameters();
  private searchTerms = new Subject<string>();
  private searchResults = new Observable<SearchResult[]>();
  private searchCount = new Observable<number>();

  constructor(
    private searchStore: SearchStore,
    private router: Router,
  ) { }

  ngOnInit() {
    this.searchParams.language = 'de';
    this.searchParams.page = 1;
    this.searchParams.page_size = this.itemsPerPage;
    this.searchTerms
      .debounceTime(300)        // wait for 300ms pause in events
      .distinctUntilChanged()   // ignore if next search term is same as previous
      .subscribe(term => {
          this.searchParams.search = term;
          this.searchStore.search(this.searchParams);
        return null;
        }
        );
    this.searchCount = this.searchStore.count;
    this.searchResults = this.searchStore.searchResults;
  }

  search(term: string): void {
    this.searchTerms.next(term);
  }

  executeSearch(event:any): void {
    this.searchParams.page = 1;
    this.getMetadataList();
  }

  pageChanged(event:any): void {
    this.searchParams.page = event.page;
    this.getMetadataList();
  }

  private getMetadataList(): void {
    this.searchStore.search(this.searchParams);
  }

}
