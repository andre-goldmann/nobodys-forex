package jdg.digital.forexbackend.domain;

import org.springframework.stereotype.Service;

import java.time.DayOfWeek;
import java.time.LocalDateTime;
import java.time.LocalTime;

@Service
public class DayTimeTradingRule {

    public boolean trade(final String symbol){
        final LocalDateTime now = LocalDateTime.now();
        final DayOfWeek day = now.getDayOfWeek();
        final LocalTime time = now.toLocalTime();

        // EURGBP rules: Monday 18:00-21:00, Tuesday 6:00-7:00, Friday 12:00-13:00
        if("EURGBP".equalsIgnoreCase(symbol)) {
            if((day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(18,0)) && time.isBefore(LocalTime.of(21,0)))) ||
               (day == DayOfWeek.TUESDAY && (!time.isBefore(LocalTime.of(6,0)) && time.isBefore(LocalTime.of(7,0)))) ||
               (day == DayOfWeek.FRIDAY && (!time.isBefore(LocalTime.of(12,0)) && time.isBefore(LocalTime.of(13,0))))) {
                return false;
            }
        }

        // EURUSD rule: Friday 6:00-7:00
        if("EURUSD".equalsIgnoreCase(symbol)) {
            if(day == DayOfWeek.FRIDAY && (!time.isBefore(LocalTime.of(6,0)) && time.isBefore(LocalTime.of(7,0)))) {
                return false;
            }
        }

        // GBPUSD rules: Wednesday 0:00-3:00 and Wednesday 4:00-7:00, Tuesday 20:00-23:00
        if("GBPUSD".equalsIgnoreCase(symbol)) {
            if((day == DayOfWeek.WEDNESDAY && ((!time.isBefore(LocalTime.of(0,0)) && time.isBefore(LocalTime.of(3,0))) ||
                                              (!time.isBefore(LocalTime.of(4,0)) && time.isBefore(LocalTime.of(7,0))))) ||
               (day == DayOfWeek.TUESDAY && (!time.isBefore(LocalTime.of(20,0)) && time.isBefore(LocalTime.of(23,0))))) {
                return false;
            }
        }

        // AUDUSD rules: Wednesday 11:00-12:00, Wednesday 18:00-19:00, Thursday 12:00-13:00, Thursday 22:00-23:00, Friday 22:00-23:00
        if("AUDUSD".equalsIgnoreCase(symbol)) {
            if((day == DayOfWeek.WEDNESDAY && ((!time.isBefore(LocalTime.of(11,0)) && time.isBefore(LocalTime.of(12,0))) ||
                                              (!time.isBefore(LocalTime.of(18,0)) && time.isBefore(LocalTime.of(19,0)))) ||
               (day == DayOfWeek.THURSDAY && ((!time.isBefore(LocalTime.of(12,0)) && time.isBefore(LocalTime.of(13,0))) ||
                                              (!time.isBefore(LocalTime.of(22,0)) && time.isBefore(LocalTime.of(23,0)))) ||
               (day == DayOfWeek.FRIDAY && (!time.isBefore(LocalTime.of(22,0)) && time.isBefore(LocalTime.of(23,0))))))) {
                return false;
            }
        }

        // USDCHF rules: sample worst hours on Monday and Thursday/Friday
        if("USDCHF".equalsIgnoreCase(symbol)) {
            if((day == DayOfWeek.MONDAY &&
                ((!time.isBefore(LocalTime.of(0,0)) && time.isBefore(LocalTime.of(1,0))) ||
                 (!time.isBefore(LocalTime.of(3,0)) && time.isBefore(LocalTime.of(4,0))) ||
                 (!time.isBefore(LocalTime.of(5,0)) && time.isBefore(LocalTime.of(6,0))) ||
                 (!time.isBefore(LocalTime.of(9,0)) && time.isBefore(LocalTime.of(10,0))) ||
                 (!time.isBefore(LocalTime.of(15,0)) && time.isBefore(LocalTime.of(16,0))))) ||
               (day == DayOfWeek.THURSDAY &&
                ((!time.isBefore(LocalTime.of(20,0)) && time.isBefore(LocalTime.of(21,0))) ||
                 (!time.isBefore(LocalTime.of(22,0)) && time.isBefore(LocalTime.of(23,0))) ||
                 (!time.isBefore(LocalTime.of(23,0)) && time.isBefore(LocalTime.of(24,0))))) ||
               (day == DayOfWeek.FRIDAY && (!time.isBefore(LocalTime.of(4,0)) && time.isBefore(LocalTime.of(5,0))))) {
                return false;
            }
        }

        // AUDNZD rule: sample worst period Monday 10:00-11:00
        if("AUDNZD".equalsIgnoreCase(symbol)) {
            if(day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(10,0)) && time.isBefore(LocalTime.of(11,0)))) {
                return false;
            }
        }

        // EURCHF rule: sample worst period Thursday 5:00-7:00 and Friday 5:00-7:00
        if("EURCHF".equalsIgnoreCase(symbol)) {
            if((day == DayOfWeek.THURSDAY || day == DayOfWeek.FRIDAY) &&
               (!time.isBefore(LocalTime.of(5,0)) && time.isBefore(LocalTime.of(7,0)))) {
                return false;
            }
        }

        // XAGUSD rule: sample rule, e.g., Wednesday at 6:00
        if("XAGUSD".equalsIgnoreCase(symbol)) {
            if(day == DayOfWeek.WEDNESDAY && time.equals(LocalTime.of(6,0))) {
                return false;
            }
        }

        // AUDJPY rules: Monday: 21-22, Monday: 22-23, Monday: 23-24, Thursday: 03-04, Tuesday: 02-03
        if("AUDJPY".equalsIgnoreCase(symbol)) {
            if(
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(21,0)) && time.isBefore(LocalTime.of(22,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(22,0)) && time.isBefore(LocalTime.of(23,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(23,0)) && time.isBefore(LocalTime.MIDNIGHT))) ||
                (day == DayOfWeek.THURSDAY && (!time.isBefore(LocalTime.of(3,0)) && time.isBefore(LocalTime.of(4,0)))) ||
                (day == DayOfWeek.TUESDAY && (!time.isBefore(LocalTime.of(2,0)) && time.isBefore(LocalTime.of(3,0))))
            ) {
                return false;
            }
        }

        // GBPAUD rules: Tuesday: 20-21, Tuesday: 19-20, Wednesday: 4-5, Wednesday: 6-7, Friday: 21-22
        if("GBPAUD".equalsIgnoreCase(symbol)) {
            if(
                (day == DayOfWeek.TUESDAY && (!time.isBefore(LocalTime.of(20,0)) && time.isBefore(LocalTime.of(21,0)))) ||
                (day == DayOfWeek.TUESDAY && (!time.isBefore(LocalTime.of(19,0)) && time.isBefore(LocalTime.of(20,0)))) ||
                (day == DayOfWeek.WEDNESDAY && (!time.isBefore(LocalTime.of(4,0)) && time.isBefore(LocalTime.of(5,0)))) ||
                (day == DayOfWeek.WEDNESDAY && (!time.isBefore(LocalTime.of(6,0)) && time.isBefore(LocalTime.of(7,0)))) ||
                (day == DayOfWeek.FRIDAY && (!time.isBefore(LocalTime.of(21,0)) && time.isBefore(LocalTime.of(22,0))))
            ) {
                return false;
            }
        }

        // NZDJPY rules: 
        // ('Tuesday', 22, -97.65)
        // ('Tuesday', 6, -90.96)
        // ('Wednesday', 4, -67.75)
        // ('Monday', 15, -35.996923076923075)
        // ('Monday', 21, -33.207142857142856)
        if("NZDJPY".equalsIgnoreCase(symbol)) {
            if(
                (day == DayOfWeek.TUESDAY && (!time.isBefore(LocalTime.of(22,0)) && time.isBefore(LocalTime.of(23,0)))) ||
                (day == DayOfWeek.TUESDAY && (!time.isBefore(LocalTime.of(6,0)) && time.isBefore(LocalTime.of(7,0)))) ||
                (day == DayOfWeek.WEDNESDAY && (!time.isBefore(LocalTime.of(4,0)) && time.isBefore(LocalTime.of(5,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(15,0)) && time.isBefore(LocalTime.of(16,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(21,0)) && time.isBefore(LocalTime.of(22,0))))
            ) {
                return false;
            }
        }

        // GBPNZD rules: 
        // Friday: 6-7 (Profit: -3731.58)
        // Thursday: 0-1 (Profit: -2854.11)
        // Thursday: 6-7 (Profit: -2772.12)
        // Thursday: 5-6 (Profit: -2688.48)
        // Wednesday: 5-6 (Profit: -2564.63)
        if("GBPNZD".equalsIgnoreCase(symbol)) {
            if(
                (day == DayOfWeek.FRIDAY && (!time.isBefore(LocalTime.of(6,0)) && time.isBefore(LocalTime.of(7,0)))) ||
                (day == DayOfWeek.THURSDAY && (!time.isBefore(LocalTime.of(0,0)) && time.isBefore(LocalTime.of(1,0)))) ||
                (day == DayOfWeek.THURSDAY && (!time.isBefore(LocalTime.of(6,0)) && time.isBefore(LocalTime.of(7,0)))) ||
                (day == DayOfWeek.THURSDAY && (!time.isBefore(LocalTime.of(5,0)) && time.isBefore(LocalTime.of(6,0)))) ||
                (day == DayOfWeek.WEDNESDAY && (!time.isBefore(LocalTime.of(5,0)) && time.isBefore(LocalTime.of(6,0))))
            ) {
                return false;
            }
        }

        // NZDUSD rules: 
        // Monday: 21-22, Sunday: 23-24, Monday: 11-12, Monday: 20-21, Monday: 19-20
        if("NZDUSD".equalsIgnoreCase(symbol)) {
            if(
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(21,0)) && time.isBefore(LocalTime.of(22,0)))) ||
                (day == DayOfWeek.SUNDAY && (!time.isBefore(LocalTime.of(23,0)) && time.isBefore(LocalTime.MIDNIGHT))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(11,0)) && time.isBefore(LocalTime.of(12,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(20,0)) && time.isBefore(LocalTime.of(21,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(19,0)) && time.isBefore(LocalTime.of(20,0))))
            ) {
                return false;
            }
        }

        // USDCAD rules:
        // Friday 22:00-23:00, Avg Profit: -58.190000000000005
        // Monday 03:00-04:00, Avg Profit: -27.81978102189781
        // Monday 00:00-01:00, Avg Profit: -25.76669902912621
        // Monday 02:00-03:00, Avg Profit: -22.335656565656567
        // Monday 09:00-10:00, Avg Profit: -18.362363636363636
        // Friday 16:00-17:00, Avg Profit: -17.629516129032258
        // Wednesday 12:00-13:00, Avg Profit: -16.83857142857143
        // Monday 11:00-12:00, Avg Profit: -16.03367469879518
        // Friday 17:00-18:00, Avg Profit: -13.307473684210526
        // Monday 01:00-02:00, Avg Profit: -12.586701570680628
        if("USDCAD".equalsIgnoreCase(symbol)) {
            if(
                (day == DayOfWeek.FRIDAY && (!time.isBefore(LocalTime.of(22,0)) && time.isBefore(LocalTime.of(23,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(3,0)) && time.isBefore(LocalTime.of(4,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(0,0)) && time.isBefore(LocalTime.of(1,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(2,0)) && time.isBefore(LocalTime.of(3,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(9,0)) && time.isBefore(LocalTime.of(10,0)))) ||
                (day == DayOfWeek.FRIDAY && (!time.isBefore(LocalTime.of(16,0)) && time.isBefore(LocalTime.of(17,0)))) ||
                (day == DayOfWeek.WEDNESDAY && (!time.isBefore(LocalTime.of(12,0)) && time.isBefore(LocalTime.of(13,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(11,0)) && time.isBefore(LocalTime.of(12,0)))) ||
                (day == DayOfWeek.FRIDAY && (!time.isBefore(LocalTime.of(17,0)) && time.isBefore(LocalTime.of(18,0)))) ||
                (day == DayOfWeek.MONDAY && (!time.isBefore(LocalTime.of(1,0)) && time.isBefore(LocalTime.of(2,0))))
            ) {
                return false;
            }
        }

        // EURAUD rules:
        // Thursday 8:00-9:00      ($-1668.6, Trades: 34)
        // Wednesday 6:00-7:00      ($-1511.92, Trades: 29)
        // Wednesday 0:00-1:00      ($-1379.23, Trades: 21)
        if("EURAUD".equalsIgnoreCase(symbol)) {
            if(
                (day == DayOfWeek.THURSDAY && (!time.isBefore(LocalTime.of(8,0)) && time.isBefore(LocalTime.of(9,0)))) ||
                (day == DayOfWeek.WEDNESDAY && (!time.isBefore(LocalTime.of(6,0)) && time.isBefore(LocalTime.of(7,0)))) ||
                (day == DayOfWeek.WEDNESDAY && (!time.isBefore(LocalTime.of(0,0)) && time.isBefore(LocalTime.of(1,0))))
            ) {
                return false;
            }
        }

        // EURCAD rules:
        // Monday: 02:00-03:00  (-49.793000, 20 trades, Total Profit: -995.86)
        // Tuesday: 00:00-01:00  (-35.740000)
        // Monday: 04:00-05:00  (-31.985000)
        // Tuesday: 04:00-05:00 (-31.117500)
        // Friday: 00:00-01:00   (-26.852727)
        // Wednesday: 13:00-14:00  (43.165000)
        // Thursday: 12:00-13:00  (43.660000)
        // Thursday: 01:00-02:00  (45.002500)
        // Thursday: 17:00-18:00  (45.550000)
        // Wednesday: 15:00-16:00  (47.486000)
        // Monday: 15:00-16:00    (-16.94906976744186, 43 trades, Total Profit: -728.81)
        // Tuesday: 07:00-08:00   (-26.339545454545455, 22 trades, Total Profit: -579.47)
        if("EURCAD".equalsIgnoreCase(symbol)) {
            if(
                (day == DayOfWeek.MONDAY && !time.isBefore(LocalTime.of(2,0)) && time.isBefore(LocalTime.of(3,0))) ||
                (day == DayOfWeek.TUESDAY && !time.isBefore(LocalTime.of(0,0)) && time.isBefore(LocalTime.of(1,0))) ||
                (day == DayOfWeek.MONDAY && !time.isBefore(LocalTime.of(4,0)) && time.isBefore(LocalTime.of(5,0))) ||
                (day == DayOfWeek.TUESDAY && !time.isBefore(LocalTime.of(4,0)) && time.isBefore(LocalTime.of(5,0))) ||
                (day == DayOfWeek.FRIDAY && !time.isBefore(LocalTime.of(0,0)) && time.isBefore(LocalTime.of(1,0))) ||
                (day == DayOfWeek.WEDNESDAY && !time.isBefore(LocalTime.of(13,0)) && time.isBefore(LocalTime.of(14,0))) ||
                (day == DayOfWeek.THURSDAY && !time.isBefore(LocalTime.of(12,0)) && time.isBefore(LocalTime.of(13,0))) ||
                (day == DayOfWeek.THURSDAY && !time.isBefore(LocalTime.of(1,0)) && time.isBefore(LocalTime.of(2,0))) ||
                (day == DayOfWeek.THURSDAY && !time.isBefore(LocalTime.of(17,0)) && time.isBefore(LocalTime.of(18,0))) ||
                (day == DayOfWeek.WEDNESDAY && !time.isBefore(LocalTime.of(15,0)) && time.isBefore(LocalTime.of(16,0))) ||
                (day == DayOfWeek.MONDAY && !time.isBefore(LocalTime.of(15,0)) && time.isBefore(LocalTime.of(16,0))) ||
                (day == DayOfWeek.TUESDAY && !time.isBefore(LocalTime.of(7,0)) && time.isBefore(LocalTime.of(8,0)))
            ) {
                return false;
            }
        }

        // GBPCHF rules:
        // Friday 06:00-07:00      (Avg Profit: -31.165256410256408)
        // Wednesday 06:00-07:00    (Avg Profit: -27.803434343434343)
        // Monday 16:00-17:00       (Avg Profit: -27.71382978723404)
        // Wednesday 02:00-03:00    (Avg Profit: -25.781190476190474)
        // Tuesday 19:00-20:00      (Avg Profit: -24.415396825396826)
        if("GBPCHF".equalsIgnoreCase(symbol)) {
            if(
                (day == DayOfWeek.FRIDAY && !time.isBefore(LocalTime.of(6,0)) && time.isBefore(LocalTime.of(7,0))) ||
                (day == DayOfWeek.WEDNESDAY && !time.isBefore(LocalTime.of(6,0)) && time.isBefore(LocalTime.of(7,0))) ||
                (day == DayOfWeek.MONDAY && !time.isBefore(LocalTime.of(16,0)) && time.isBefore(LocalTime.of(17,0))) ||
                (day == DayOfWeek.WEDNESDAY && !time.isBefore(LocalTime.of(2,0)) && time.isBefore(LocalTime.of(3,0))) ||
                (day == DayOfWeek.TUESDAY && !time.isBefore(LocalTime.of(19,0)) && time.isBefore(LocalTime.of(20,0)))
            ) {
                return false;
            }
        }

        // CADJPY rules:
        // Tuesday 18:00-19:00      (Avg Profit: -67.09166666666667)
        // Tuesday 17:00-18:00      (Avg Profit: -65.32833333333333)
        // Tuesday 23:00-24:00      (Avg Profit: -64.98375)
        // Wednesday 1:00-2:00      (Avg Profit: -63.69833333333333)
        // Wednesday 0:00-1:00      (Avg Profit: -63.195)
        // Tuesday 21:00-22:00      (Avg Profit: -58.72714285714285)
        // Wednesday 2:00-3:00      (Avg Profit: -58.129999999999995)
        if("CADJPY".equalsIgnoreCase(symbol)) {
            if(
                (day == DayOfWeek.TUESDAY && !time.isBefore(LocalTime.of(18,0)) && time.isBefore(LocalTime.of(19,0))) ||
                (day == DayOfWeek.TUESDAY && !time.isBefore(LocalTime.of(17,0)) && time.isBefore(LocalTime.of(18,0))) ||
                (day == DayOfWeek.TUESDAY && !time.isBefore(LocalTime.of(23,0)) && time.isBefore(LocalTime.MIDNIGHT)) ||
                (day == DayOfWeek.WEDNESDAY && !time.isBefore(LocalTime.of(1,0)) && time.isBefore(LocalTime.of(2,0))) ||
                (day == DayOfWeek.WEDNESDAY && !time.isBefore(LocalTime.of(0,0)) && time.isBefore(LocalTime.of(1,0))) ||
                (day == DayOfWeek.TUESDAY && !time.isBefore(LocalTime.of(21,0)) && time.isBefore(LocalTime.of(22,0))) ||
                (day == DayOfWeek.WEDNESDAY && !time.isBefore(LocalTime.of(2,0)) && time.isBefore(LocalTime.of(3,0)))
            ) {
                return false;
            }
        }

        // NZDCAD rule: sample rule, e.g., Friday 19:00-20:00
        if("NZDCAD".equalsIgnoreCase(symbol)) {
            if(day == DayOfWeek.FRIDAY && (!time.isBefore(LocalTime.of(19,0)) && time.isBefore(LocalTime.of(20,0)))) {
                return false;
            }
        }

        return true;
    }
}
