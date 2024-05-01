import type { Meta, StoryObj } from '@storybook/angular';
import { InputComponent } from './input-component.component';

import { within } from '@storybook/testing-library';
import { expect } from '@storybook/jest';
import {FormControl} from "@angular/forms";

const meta: Meta<InputComponent> = {
  component: InputComponent,
  title: 'InputComponentComponent',
};
export default meta;
type Story = StoryObj<InputComponent>;

export const Primary: Story = {
  args: {
    control: new FormControl(''),
    containerClassName: '',
    icon: '',
    iconSize: 'md',
    placeholder: '',
    rounded: false,
    enableClearButton: false,
    autoFocus: false,
  },
};

export const Heading: Story = {
  args: {
    control: new FormControl(''),
    containerClassName: '',
    icon: '',
    iconSize: 'md',
    placeholder: '',
    rounded: false,
    enableClearButton: false,
    autoFocus: false,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    expect(canvas.getByText(/input-component works!/gi)).toBeTruthy();
  },
};
