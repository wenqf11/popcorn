package cn.edu.tsinghua.thss.popcorn;

import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentTransaction;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.roomorama.caldroid.CaldroidFragment;
import com.roomorama.caldroid.CaldroidListener;

import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

import cn.edu.tsinghua.thss.popcorn.config.Config;


public class BonusHistoryActivity extends FragmentActivity {
    CaldroidFragment caldroidFragment;
    Date lastSelected = null;
    TextView resultText;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bonus_history);

        resultText = (TextView)findViewById(R.id.bonus_result);

        caldroidFragment = new CaldroidFragment();
        Bundle args = new Bundle();
        Calendar cal = Calendar.getInstance();
        args.putInt(CaldroidFragment.MONTH, cal.get(Calendar.MONTH) + 1);
        args.putInt(CaldroidFragment.YEAR, cal.get(Calendar.YEAR));
        caldroidFragment.setArguments(args);

        updateResultText(cal.getTime());
        caldroidFragment.setCaldroidListener(new CaldroidListener() {
            @Override
            public void onSelectDate(Date date, View view) {
                caldroidFragment.setBackgroundResourceForDate(R.color.light_blue, date);
                if(lastSelected!=null && lastSelected.compareTo(date)!=0){
                    caldroidFragment.clearBackgroundResourceForDate(lastSelected);
                }
                lastSelected = date;
                caldroidFragment.refreshView();
                resultText.setText("");
                updateResultText(date);
            }
        });

        android.support.v4.app.FragmentTransaction t = getSupportFragmentManager().beginTransaction();
        t.replace(R.id.bonus_calendar, caldroidFragment);
        t.commit();
    }

    private void updateResultText(Date date){

        String date_str = String.format("%tF", date);

        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);
        params.addQueryStringParameter("date", date_str);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.GET_BONUS_INFO_URL,
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

                        try{
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");

                            if(status.equals("ok")) {
                                JSONObject bonusInfo = jsonObject.getJSONObject("data");
                                String state = bonusInfo.getString("state");
                                String bonus = bonusInfo.getString("bonus");
                                if(state.equals("0")){
                                    resultText.setText("未中奖");
                                } else if(state.equals("1")) {
                                    resultText.setText("中奖金额"+bonus+"元，尚未领取。");
                                } else if(state.equals("2")) {
                                    resultText.setText("中奖金额"+bonus+"元，已经领取。");
                                }
                            }
                            else{
                                resultText.setText("这天没有参与抽奖");
                            }
                        }catch (JSONException e){
                            e.printStackTrace();
                        }
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), "网络故障或服务器内部错误", Toast.LENGTH_SHORT).show();
                    }
                });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_bonus_history, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            BonusHistoryActivity.this.finish();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
