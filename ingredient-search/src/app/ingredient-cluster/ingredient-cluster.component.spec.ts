import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IngredientClusterComponent } from './ingredient-cluster.component';

describe('IngredientClusterComponent', () => {
  let component: IngredientClusterComponent;
  let fixture: ComponentFixture<IngredientClusterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IngredientClusterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(IngredientClusterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
