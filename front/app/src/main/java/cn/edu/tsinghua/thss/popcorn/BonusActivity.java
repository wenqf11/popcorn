package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;

import org.json.JSONException;
import org.json.JSONObject;

import cn.edu.tsinghua.thss.popcorn.config.Config;


public class BonusActivity extends Activity {
    @ViewInject(R.id.get_lottery_btn)
    private Button mButtonGetLottery;

    @OnClick(R.id.get_lottery_btn)
    private void getLotteryButtonClick(View v) {
        SharedPreferences sp = getApplicationContext().getSharedPreferences("BonusData", MODE_PRIVATE);
        int times = sp.getInt("lottery_times", 0);
        if(times > 0) {
            getBonus();
        } else {
            new AlertDialog.Builder(BonusActivity.this)
                    .setTitle("没有抽奖机会，不能抽奖！")
                    .setPositiveButton("确定", null)
                    .show();
        }
    }

    @ViewInject(R.id.get_lottery_history_btn)
    private Button getHistoryBtn;

    @OnClick(R.id.get_lottery_history_btn)
    private void onGetHistoryBtnClick(View v) {
        Intent intent = new Intent(this, BonusHistoryActivity.class);
        startActivity(intent);
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bonus);
        ViewUtils.inject(this);
        setLotteryTimes();
    }

    private void setLotteryTimes(){
        SharedPreferences sp = getApplicationContext().getSharedPreferences("BonusData", MODE_PRIVATE);
        int times = sp.getInt("lottery_times", 0);
        if(times >= 0) {
            mButtonGetLottery.setText("抽奖（"+times+"）");
        }
    }

    private void getBonus(){
        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.GET_BONUS_URL,
                params,
                new RequestCallBack<String>() {

                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");

                            if (status.equals("ok")) {
                                JSONObject bonusInfo = jsonObject.getJSONObject("data");
                                String result = bonusInfo.getString("result");
                                String bonus = bonusInfo.getString("bonus");
                                if (result.equals("false")) {
                                    new AlertDialog.Builder(BonusActivity.this)
                                            .setTitle("很遗憾，您没有中奖，下次再来！")
                                            .setPositiveButton("确定", null)
                                            .show();
                                } else {
                                    new AlertDialog.Builder(BonusActivity.this)
                                            .setTitle("恭喜中奖！金额为" + bonus + "元。")
                                            .setPositiveButton("确定", null)
                                            .show();
                                }

                                SharedPreferences sp = getApplicationContext().getSharedPreferences("BonusData", MODE_PRIVATE);
                                int times = sp.getInt("lottery_times", 0) - 1;
                                SharedPreferences.Editor editor = sp.edit();
                                editor.putInt("lottery_times", times);
                                editor.apply();
                                if(times >= 0) {
                                    mButtonGetLottery.setText("抽奖（"+times+"）");
                                }
                            } else {
                                new AlertDialog.Builder(BonusActivity.this)
                                        .setTitle("不能重复抽奖！")
                                        .setPositiveButton("确定", null)
                                        .show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                    }
                });
    }

    @Override
    protected  void onDestroy(){
        super.onDestroy();
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.bonus, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            BonusActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
