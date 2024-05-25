package jdg.digital.forexbackend.domain.model;

import jakarta.persistence.*;

import java.time.LocalDateTime;
import java.util.Objects;

@Entity
@Table(name = "\"ProdTrades\"")
public class ProdTradeEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "symbol")
    private String symbol;

    @Column(name = "type")
    private String type;

    @Column(name = "entry")
    private Double entry;

    @Column(name = "sl")
    private Double sl;

    @Column(name = "tp")
    private Double tp;

    @Column(name = "lots")
    private Double lots;

    @Column(name = "spread")
    private Double spread;

    @Column(name = "tradeid")
    private Integer tradeId;

    @Column(name = "stamp")
    private LocalDateTime stamp;

    @Column(name = "activated")
    private String activated;

    @Column(name = "openprice")
    private Double openprice;

    @Column(name = "swap")
    private Double swap;

    @Column(name = "profit")
    private Double profit;

    @Column(name = "closed")
    private String closed;

    @Column(name = "commision")
    private Double commision;

    @Column(name = "strategy")
    private String strategy;

    @Column(name = "exit")
    private Double exit;

    protected ProdTradeEntity() {
    }

    public ProdTradeEntity(
            final String symbol,
            final String type,
            final Double entry,
            final Double sl,
            final Double tp,
            final Double lots,
            final String strategy) {
        this.symbol = symbol;
        this.type = type;
        this.entry = entry;
        this.sl = sl;
        this.tp = tp;
        this.lots = lots;
        this.strategy = strategy;
        this.stamp = LocalDateTime.now();
    }

    public String getSymbol() {
        return symbol;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Double getEntry() {
        return entry;
    }

    public void setEntry(Double entry) {
        this.entry = entry;
    }

    public Double getSl() {
        return sl;
    }

    public void setSl(Double sl) {
        this.sl = sl;
    }

    public Double getTp() {
        return tp;
    }

    public void setTp(Double tp) {
        this.tp = tp;
    }

    public Double getLots() {
        return lots;
    }

    public void setLots(Double lots) {
        this.lots = lots;
    }

    public Double getSpread() {
        return spread;
    }

    public void setSpread(Double spread) {
        this.spread = spread;
    }

    public Integer getTradeId() {
        return tradeId;
    }

    public void setTradeId(Integer tradeId) {
        this.tradeId = tradeId;
    }

    public LocalDateTime getStamp() {
        return stamp;
    }

    public void setStamp(LocalDateTime stamp) {
        this.stamp = stamp;
    }

    public String getActivated() {
        return activated;
    }

    public void setActivated(String activated) {
        this.activated = activated;
    }

    public Double getOpenprice() {
        return openprice;
    }

    public void setOpenprice(Double openprice) {
        this.openprice = openprice;
    }

    public Double getSwap() {
        return swap;
    }

    public void setSwap(Double swap) {
        this.swap = swap;
    }

    public Double getProfit() {
        return profit;
    }

    public void setProfit(Double profit) {
        this.profit = profit;
    }

    public String getClosed() {
        return closed;
    }

    public void setClosed(String closed) {
        this.closed = closed;
    }

    public Double getCommision() {
        return commision;
    }

    public void setCommision(Double commision) {
        this.commision = commision;
    }

    public String getStrategy() {
        return strategy;
    }

    public void setStrategy(String strategy) {
        this.strategy = strategy;
    }

    public Double getExit() {
        return exit;
    }

    public void setExit(Double exit) {
        this.exit = exit;
    }

    @Override
    public String toString() {
        return "ProdTradeEntity{" +
                "exit=" + exit +
                ", strategy='" + strategy + '\'' +
                ", commision=" + commision +
                ", closed='" + closed + '\'' +
                ", profit=" + profit +
                ", swap=" + swap +
                ", openprice=" + openprice +
                ", activated='" + activated + '\'' +
                ", stamp=" + stamp +
                ", tradeId=" + tradeId +
                ", spread=" + spread +
                ", lots=" + lots +
                ", tp=" + tp +
                ", sl=" + sl +
                ", entry=" + entry +
                ", type='" + type + '\'' +
                ", symbol='" + symbol + '\'' +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ProdTradeEntity that = (ProdTradeEntity) o;
        return Objects.equals(id, that.id) && Objects.equals(symbol, that.symbol) && Objects.equals(stamp, that.stamp) && Objects.equals(strategy, that.strategy);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, symbol, stamp, strategy);
    }
}