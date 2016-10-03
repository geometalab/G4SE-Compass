import { Component, OnInit } from '@angular/core';
import {SearchResult} from "./search-result";
import {Router} from "@angular/router";
import {SearchParameters} from "./search-parameters";
import {SearchService} from "./search.service";

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  searchResultList: SearchResult[];
  error: any;
  totalItems:number = 0;
  currentPage:number = 1;
  language: string = 'de';
  ordering: string = null;
  showSpinner: boolean = true;
  // pagination settings
  private itemsPerPage: number = 10;
  maxSize: number = 5; // maxNumberButtonsVisible

  private searchParams: SearchParameters = new SearchParameters();

  constructor(
    private searchService: SearchService,
    private router: Router
  ) { }

  ngOnInit() {
    this.searchParams.language = 'de';
    this.searchParams.page = 1;
    this.executeSearch();
  }

  executeSearch(): void {
    this.getMetadataList();
  }

  languageChanged(): void {
    this.executeSearch();
  }

  pageChanged(): void {
    this.executeSearch();
  }


  private processData(searchResults): void {
    this.searchResultList = searchResults.results;
    this.totalItems = searchResults.count;
    console.log(searchResults);
  }

  private getMetadataList(): void {
    this.searchService
      .getSearchResultList(this.searchParams)
      .then(searchResults => this.processData(searchResults))
      .catch(error => this.error = error);
  }


}
